from threading import local

from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()
base_thread = local()


class BaseModel(base):
    __abstract__ = True
    shard_thread = base_thread
    shard_thread.shard = "hitmancompany"

    @classmethod
    def get_shard(cls):
        return "hitmancompany"


class HitmanCompanyModel(BaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "hitmancompany"}
