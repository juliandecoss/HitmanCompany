from flask import Flask, json, jsonify, request
from werkzeug.exceptions import HTTPException

from encrypt import check_password
from exception import ForbiddenException, HitmanException, MissingParameterException
from tokens import create_token, validate_token
from transactions import (create_hit_job, create_user, get_all_hits,
                          get_all_hits_by_hitman, get_all_hits_by_manager,
                          get_hit_by_id, get_hitmans_by_boss,
                          get_hitmans_by_manager_id, get_user, get_user_by_id,
                          merge_new_hitman_in_job
                          )
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/")
def hello_world():
    return "Hitman Api Healthy"


@app.route("/login", methods=["POST"])
def login():
    input_json = request.get_json(force=True)
    print(f"Si llego aquí con este json {input_json}")
    email = input_json["email"]
    password = input_json["password"]
    user = get_user(email)
    if not user or not check_password(password, user.password):
        raise HitmanException
    access_token = create_token(user)
    return jsonify({"message": "Successful login", "access_token": access_token})


@app.route("/register", methods=["POST"])
def register():
    input_json = request.get_json(force=True)
    user = create_user(input_json)
    return jsonify({"message": "Successful user created", "user_id": user.id})


@app.route("/hits", methods=["POST"])
def get_hits():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        role = token["role"]
        if id == 1:
            jobs = get_all_hits()
        elif role == "Hitman":
            jobs = get_all_hits_by_hitman(id)
        elif role == "Manager":
            jobs = get_all_hits_by_manager(id)
        hits_parsed = []
        if jobs:
            for job in jobs:
                res = {}
                res["job_id"] = job.job_id
                res["assigned_to"] = job.assigned_to
                res["assigned_by"] = job.assigned_by
                hits_parsed.append(res)
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify({"message": "Successful hits retrieved", "hits": hits_parsed})


@app.route("/hits/id", methods=["POST"])
def get_unique_hit():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
        hit_id = json["job_id"]
        print(hit_id)
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        role = token["role"]
        if id == 1:
            job = get_hit_by_id(hit_id)
            if not job:
                raise ForbiddenException
        elif role == "Hitman":
            job = get_hit_by_id(hit_id)
            if not job or job.assigned_to != id:
                if not job:
                    print("This job does not exist")
                else:
                    print(f"Hitman Job is not with id {id}, is with: {job.assigned_to}")
                raise ForbiddenException
        elif role == "Manager":
            job = get_hit_by_id(hit_id)
            if not job or job.assigned_by != id:
                if not job:
                    print("This job does not exist")
                else:
                    print(f"Manager Job is not with id {id}, is with: {job.assigned_by}")
                raise ForbiddenException
        hit_parsed = {}
        hit_parsed["hit_id"] = job.job_id
        hit_parsed["assigned_by"] = job.assigned_by
        hit_parsed["assigned_to"] = job.assigned_to
        hit_parsed["description"] = job.description
        hit_parsed["status_job"] = job.status_job
        hit_parsed["target_name"] = job.target_name
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify({"message": "Successful hits retrieved", "hits": hit_parsed})


@app.route("/hits/create", methods=["POST"])
def create_hit():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
        assigned_to = json["assigned_to"]
        json["name_to_kill"]
        json["description"]
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        role = token["role"]
        if id == 1:
            manager_id = 2
            job = create_hit_job(json, manager_id)
        elif role == "Hitman":
            print(f"The hitman not allowed to create hits")
            raise ForbiddenException
        elif role == "Manager":
            hitmans = get_hitmans_by_manager_id(id)
            hitman_ids = []
            for hitman in hitmans:
                hitman_ids.append(hitman.Users.id)
            if assigned_to not in hitman_ids:
                print(
                    f"The hitman id {assigned_to} doesnt belong to manager {id} with hitmans={hitman_ids}"
                )
                raise ForbiddenException
            job = create_hit_job(json, id)
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify(
        {
            "message": "Successful hit created",
            "job_id": job.job_id,
            "assigned_to": job.assigned_to,
        }
    )


@app.route("/hitmen", methods=["POST"])
def get_hitmen_list():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        role = token["role"]
        if id == 1:
            """"""
            hitmans = get_hitmans_by_boss()
        elif role == "Hitman":
            print(f"The hitman not allowed to see hitmen")
            raise ForbiddenException
        elif role == "Manager":
            hitmans = get_hitmans_by_manager_id(id)
        res = []
        for hitman in hitmans:
            hitman_data = {}
            hitman_data["id"] = hitman.Users.id
            hitman_data["name"] = hitman.Users.name
            hitman_data["email"] = hitman.Users.email
            hitman_data["manager_id"] = hitman.Teams.manager_id
            res.append(hitman_data)
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify(
        {
            "message": "Successful hitmans retrieved",
            "res": res,
        }
    )


@app.route("/hitmen/id", methods=["POST"])
def get_hitmen_id():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
        hitman_id = json["hitman_id"]
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        role = token["role"]
        if id == 1:
            """"""
            hitman = get_user_by_id(hitman_id)
        elif role == "Hitman":
            print(f"The hitman not allowed to see hitmen")
            raise ForbiddenException
        elif role == "Manager":
            hitmans = get_hitmans_by_manager_id(id)
            hitman_ids = []
            for hitman in hitmans:
                hitman_ids.append(hitman.Teams.hitman_id)
            if hitman_id not in hitman_ids:
                print(
                    f"The hitman id {hitman_id} doesnt belong to manager {hitman_ids}"
                )
                raise ForbiddenException
            hitman = get_user_by_id(hitman_id)
        hitman_data = {}
        hitman_data["id"] = hitman.id
        hitman_data["name"] = hitman.name
        hitman_data["email"] = hitman.email
        hitman_data["description"] = hitman.description
        hitman_data["status"] = hitman.user_status
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify(
        {
            "message": "Successful hitmans retrieved",
            "res": hitman_data,
        }
    )

@app.route("/hitmen/bulk", methods=["POST"])
def change_hitmen():
    json = request.get_json(force=True)
    try:
        access_token = json["access_token"]
        hit_id = json["job_id"]
        new_hitman_id = json["hitman_id"]
    except KeyError as e:
        print(e)
        raise MissingParameterException
    try:
        token = validate_token(access_token)
        id = token["id"]
        if id == 1:
            job = merge_new_hitman_in_job(hit_id,new_hitman_id)
            hit_parsed = {}
            hit_parsed["hit_id"] = job.job_id
            hit_parsed["assigned_by"] = job.assigned_by
            hit_parsed["assigned_to"] = job.assigned_to
            hit_parsed["description"] = job.description
            hit_parsed["status_job"] = job.status_job
            hit_parsed["target_name"] = job.target_name
        else:
            print("None manager or hitman can change assign")
            raise ForbiddenException
    except Exception as e:
        print(e)
        raise ForbiddenException
    return jsonify(
        {
            "message": "Successful hit updated",
            "res": hit_parsed,
        }
    )