from sqlalchemy import Column, DefaultClause, Integer, String

from base_model import HitmanCompanyModel


class Users(HitmanCompanyModel):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column("email", String(255))
    name = Column("name", String(255))
    password = Column(String(128), DefaultClause(""), nullable=False)
    description = Column(String(255))
    user_status = Column("user_status", String(255), DefaultClause("Active"))
    role = Column("role", String(255), DefaultClause("Hitman"))


class Jobs(HitmanCompanyModel):

    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True)
    assigned_to = Column(Integer, nullable=False)
    assigned_by = Column(Integer, nullable=False)
    description = Column(String(255))
    status_job = Column(String(255), DefaultClause("Assigned"))
    target_name = Column("target_name", String(255))


class Teams(HitmanCompanyModel):

    __tablename__ = "teams"

    relation_id = Column(Integer, primary_key=True)
    hitman_id = Column(Integer, nullable=False)
    manager_id = Column(Integer, nullable=False)
