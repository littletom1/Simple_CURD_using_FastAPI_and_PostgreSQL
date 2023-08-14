import uuid
from cores.postgresql.connection import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
