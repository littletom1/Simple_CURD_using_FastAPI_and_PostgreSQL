from pydantic import BaseModel, conint
from typing import Generic, TypeVar, Optional, List
from pydantic.generics import GenericModel
from fastapi import Query, Depends, FastAPI
from pydantic.dataclasses import dataclass
T = TypeVar("T")

class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = '200'
        self.message = 'Success'
        return self

class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.code = '200'
        self.message = 'Success'
        self.data = data
        return self




class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int

class PaginationParams(BaseModel):
    page_size: Optional[conint(gt=0, lt=99999)] = 10
    page: Optional[conint(gt=0)] = 1
    sort_by: Optional[str] = 'created_at'
    order: Optional[str] = 'desc'

class PageResponseSchema(BaseModel):
    metadata: MetadataSchema
    # data: List[]
@dataclass
class QueryParams:
    req1: float = Query(...)
    opt1: int = Query(None)
    req_list: List[str] = Query(...)
