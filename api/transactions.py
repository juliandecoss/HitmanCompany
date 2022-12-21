from exception import MissingParameterException
from orm import Jobs, Teams, Users
from sql_alchemy import session
from encrypt import encrypt


def create_user(user_data: dict):
    try:
        user = Users()
        user.email = user_data["email"]
        user.name = user_data["name"]
        user.password = encrypt(user_data["password"])
        user.description = user_data["description"]
        if user_data.get("role"):
            user.role = user_data["role"]
        session.add(user)

        session.commit()
        session.flush()
    except Exception as e:
        print(e)
        raise MissingParameterException
    print(f"Successful user created with role {user.role or 'Hitman'}")
    return user


def get_user(email: str) -> Users:
    session.flush()
    return session.query(Users).filter(Users.email == email).first()


def get_user_by_id(id: int) -> Users:
    return session.query(Users).filter(Users.id == id).first()


def create_hit_job(json: dict, id: int) -> Jobs:
    job = Jobs()
    job.assigned_by = id
    job.assigned_to = json["assigned_to"]
    job.description = json["description"]
    job.target_name = json["name_to_kill"]
    session.add(job)

    session.commit()
    return job


def get_hitmans_by_manager_id(manager_id: int):
    return (
        session.query(Teams, Users)
        .filter(Teams.manager_id == manager_id, Teams.hitman_id == Users.id)
        .all()
    )


def get_hitmans_by_boss():
    return (
        session.query(Users, Teams)
        .filter(Users.role == "Hitman", Users.id == Teams.hitman_id)
        .all()
    )


def get_all_hitmans():
    return session.query(Teams).all()


def get_all_hits():
    return session.query(Jobs).all()


def get_all_hits_by_hitman(hitman_id):
    return session.query(Jobs).filter(Jobs.assigned_to == hitman_id).all()


def get_all_hits_by_manager(manager_id):
    return session.query(Jobs).filter(Jobs.assigned_by == manager_id).all()


def get_hit_by_id(hit_id) -> Jobs:
    job = session.query(Jobs).filter(Jobs.job_id == hit_id).first()
    return job

def merge_new_hitman_in_job(hit_id:int,new_hitman_id:int)->Jobs:
    hit = get_hit_by_id(hit_id)
    hit.assigned_to = new_hitman_id
    session.merge(hit)
    session.commit()
    return hit

# hit = get_hit_by_id(3)
# breakpoint()