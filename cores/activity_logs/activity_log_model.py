from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from cores.models.base_model import Base
class ActivityLog(Base):
    __tablename__ = 'activity_log'
    id = Column(Integer, primary_key=True, autoincrement=True)

    event = Column(String(50), nullable=True)
    log_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    subject_id = Column(Integer, nullable=True)
    subject_type = Column(String(255), nullable=True)
    causer_id = Column(Integer, nullable=True)
    # causer_type = Column(String(255), nullable=True)
    properties = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
