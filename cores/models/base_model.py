from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime
from db import Base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from decouple import config
class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    _the_prefix = config('db_prefix_database', '')
    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    @hybrid_property
    def active(self):
        return self.deleted_at == None
