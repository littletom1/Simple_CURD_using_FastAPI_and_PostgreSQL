import logging
from pydantic import BaseModel, conint, Extra
from abc import ABC, abstractmethod
from typing import Optional, Generic, Sequence, Type, TypeVar

from pydantic.generics import GenericModel
from contextvars import ContextVar
from cores.schemas.sche_base import ResponseSchemaBase, MetadataSchema
from cores.helpers.exception_handler import CustomResponse

T = TypeVar("T")
C = TypeVar("C")

logger = logging.getLogger()


class PaginationParams(BaseModel):
    page_size: Optional[conint(gt=0, lt=99999)] = 10
    page: Optional[conint(gt=0)] = 1
    sort_by: Optional[str] = 'id'
    order: Optional[str] = 'desc'
    #
    # class Config:
    #     allow_population_by_field_name = True
    #     extra = Extra.allow

class BasePage(ResponseSchemaBase, GenericModel, Generic[T], ABC):
    data: Sequence[T]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    @abstractmethod
    def create(cls: Type[C], code: str, message: str, data: Sequence[T], metadata: MetadataSchema) -> C:
        pass  # pragma: no cover


class Page(BasePage[T], Generic[T]):
    metadata: MetadataSchema

    @classmethod
    def create(cls, code: str, message: str, data: Sequence[T], metadata: MetadataSchema) -> "Page[T]":
        return cls(
            code=code,
            message=message,
            data=data,
            metadata=metadata
        )


PageType: ContextVar[Type[BasePage]] = ContextVar("PageType", default=Page)


async def paginate(db, model, query, params: Optional[PaginationParams]) -> BasePage:
    from sqlalchemy import asc, desc, func
    from sqlalchemy.future import select
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import func
    code = '200'
    message = 'Success'
    executed = await db.execute(select(func.count()).select_from(query.subquery()))
    total = executed.scalar()
    query = query.limit(params.page_size).offset(params.page_size * (params.page-1))

    if hasattr(params, 'order'):
        direction = desc if params.order == 'desc' else asc
        query = query.order_by(direction(getattr(model, params.sort_by)))


    executed = await db.execute(query)
    data = executed.scalars().unique().all()

    metadata = MetadataSchema(
        current_page=params.page,
        page_size=params.page_size,
        total_items=total
    )

    return PageType.get().create(code, message, data, metadata)