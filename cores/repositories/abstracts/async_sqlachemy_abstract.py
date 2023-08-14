from fastapi import HTTPException, status, Depends, BackgroundTasks
from abc import ABCMeta, abstractmethod
from ..contracts.repository_contract import SqlAchemyContracts
from cores.helpers.async_paging import paginate
from sqlalchemy.sql import func, update, delete
from sqlalchemy import asc, desc
from cores.helpers import helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class SqlAchemyAbstract(SqlAchemyContracts):
    __metaclass__ = ABCMeta
    _model = None

    # def __init__(self):
    #     db = next(get_db())
    # # def __init__(self, db: AsyncSession, model,
    # #             activity_log: ActivityLog = Depends(ActivityLog)):
    # #     self.service = activity_log
    # #     pass

    @abstractmethod
    def get_model(self):
        return self._model

    @abstractmethod
    def set_model(self, model):
        self._model = model

    @abstractmethod
    async def get_all(self, db: AsyncSession, with_trash: bool = False, options=[]):
        query = select(self._model).options(*options)
        if not with_trash:
            query = query.where(self._model.deleted_at.is_(None))

        executed = await db.execute(query)
        return executed.scalars().all()

    @abstractmethod
    async def paginate(self, db: AsyncSession, params_pagination, params=None, with_trash: bool = False, options=[]):
        try:
            query = select(self._model).options(*options)
            if params:
                for key, param in params:
                    if param:
                        if type(param) is int:
                            query = query.where(getattr(self._model, key) == param)
                        else:
                            query = query.where(getattr(self._model, key).ilike(f'%{param}%'))
            if hasattr(params_pagination, 'except_ids') and params_pagination.except_ids:
                except_ids = params_pagination.except_ids.split(',')
                query = query.where(self._model.id.not_in(except_ids))
            if hasattr(params_pagination, 'exist_ids') and params_pagination.exist_ids:
                exist_ids = params_pagination.exist_ids.split(',')
                query = query.where(self._model.id.in_(exist_ids))
            # if len(params) > 0:
            #     for key, value in params.items():
            #         print(key, value)
            if not with_trash:
                query = query.where(self._model.deleted_at.is_(None))
            data = await paginate(db, self._model, query, params_pagination)

            return data
        except:
            await db.rollback()
            raise

    @abstractmethod
    async def find(self, db: AsyncSession, id: int, with_trash: bool = False, options=[]):
        print(options)
        query = select(self._model).where(self._model.id == id).options(*options)
        # if options:
        #     for option in options:
        #         query = query.options(joinedload(self._model.users))
        if not with_trash:
            query = query.where(self._model.deleted_at.is_(None))
        executed = await db.execute(query)

        obj = executed.scalar()
        return obj

    @abstractmethod
    async def get_by_user_id(self, db: AsyncSession, user_id, is_get_first: bool = False, is_primary: bool = False,
                             with_trash: bool = False, order='asc', options=[]):
        direction = desc if order == 'desc' else asc
        query = select(self._model).options(*options).where(self._model.user_id == user_id).order_by(
            direction('created_at'))

        if is_primary:
            query = query.where(self._model.is_primary)

        if not with_trash:
            query = query.where(self._model.deleted_at.is_(None))
        executed = await db.execute(query)
        if not is_get_first:
            return executed.scalars().all()
        return executed.scalar()

    @abstractmethod
    async def search(self, db: AsyncSession, fields: dict = {}, is_absolute: bool = False, is_get_first=True,
                     options=[]):
        query = select(self._model).options(*options)
        if fields:
            for k, v in fields.items():
                if v:
                    if type(v) == int:
                        query = query.where(getattr(self._model, k) == v)
                    else:
                        v = v.strip()
                        if is_absolute:
                            query = query.where(getattr(self._model, k).ilike(f'{v}'))
                        else:
                            query = query.where(getattr(self._model, k).ilike(f'%{v}%'))
        executed = await db.execute(query)
        if is_get_first:
            return executed.scalar()
        # if not obj:
        #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object is not available")
        return executed.scalars().all()

    @abstractmethod
    async def create(self, db: AsyncSession, data):
        if isinstance(data, self._model):
            pass
        else:
            if type(data) is dict:
                data_to_dict = data
            else:
                data_to_dict = data.dict()
            data = self._model(**data_to_dict)
            if hasattr(self._model, 'created_at') and str(self._model.created_at.type) == 'INTEGER':
                current_time = helper.get_current_time_as_int()
                data.created_at = current_time
                data.updated_at = current_time
        try:
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data
        except:
            await db.rollback()
            raise

    @abstractmethod
    async def update(self, db: AsyncSession, id, data, with_restore: bool = False):
        if not await self.find(db, id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Object with the id: {id} is not available")
        try:
            if type(data) is not dict:
                data = data.dict()
            if hasattr(self._model, 'created_at') and str(self._model.updated_at.type) == 'INTEGER':
                current_time = helper.get_current_time_as_int()
                data['updated_at'] = current_time

            if 'token' in data:
                data.pop('token')

            if with_restore:
                data['deleted_at'] = None
            # q_obj.update(data)
            q_obj = (update(self._model).where(self._model.id == id)
                     .values(data)
                     .execution_options(synchronize_session='fetch'))
            executed = await db.execute(q_obj)
            await db.commit()
            return await self.find(db, id)

        except Exception as e:
            print(e)
            await db.rollback()
            raise

    @abstractmethod
    async def delete(self, db: AsyncSession, id, is_hard_delete: bool = False):
        if not await self.find(db, id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Object with the id: {id} is not available")
        if not is_hard_delete:
            if hasattr(self._model, 'deleted_at') and str(self._model.deleted_at.type) == 'INTEGER':
                current_time = helper.get_current_time_as_int()
            else:
                current_time = func.now()
            q_obj = (update(self._model).where(self._model.id == id)
                     .values({'deleted_at': current_time})
                     .execution_options(synchronize_session='fetch'))
            executed = await db.execute(q_obj)
        else:
            q_obj = (delete(self._model).where(self._model.id == id)
                     .execution_options(synchronize_session='fetch'))
            executed = await db.execute(q_obj)
        await db.commit()
        # db.refresh(obj)

        return await self.search(db, {'id': id})
