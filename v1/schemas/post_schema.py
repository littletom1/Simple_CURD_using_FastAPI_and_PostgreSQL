from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr

class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str

    class Config:
        orm_mode = True


class CreatePostSchema(PostBaseSchema):
    pass


class PostResponse(PostBaseSchema):
    id: int
    # created_at: datetime
    # updated_at: datetime


class UpdatePostSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    # created_at: datetime | None = None
    # updated_at: datetime | None = None

    class Config:
        orm_mode = True
        
        