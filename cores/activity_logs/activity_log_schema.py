from pydantic import BaseModel, Json
from typing import Optional, Any
from datetime import datetime

class ActivityLogBase(BaseModel):
    event: Optional[str] = None
    log_name: Optional[str] = None
    description: Optional[str] = None
    subject_id: Optional[int] = None
    subject_type: Optional[str] = None
    causer_id: Optional[int] = None
    properties: Optional[Json[Any]] = None

    class Config:
        orm_mode = True

class ActivityLogResponse(ActivityLogBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ActivityLogCreateRequest(ActivityLogBase):
    class Config:
        orm_mode = True
        # schema_extra = {
        #     "example": {
        #         "name": "pos name test",
        #     }
        # }

class ActivityLogUpdateRequest(ActivityLogBase):
    class Config:
        orm_mode = True
        # schema_extra = {
        #     "example": {
        #         "name": "pos name test update",
        #     }
        # }
