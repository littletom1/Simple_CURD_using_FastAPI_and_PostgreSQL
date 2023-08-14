from fastapi import HTTPException, status, Depends, BackgroundTasks
from abc import ABCMeta, abstractmethod
from ..contracts.repository_contract import SqlAchemyContracts
from cores.helpers.paging import paginate
from sqlalchemy.sql import func
from sqlalchemy import asc, desc
from cores.helpers import helper
from sqlalchemy.orm import Session
class SqlAchemyAbstract(SqlAchemyContracts):
    __metaclass__ = ABCMeta
    _model = None
    # def __init__(self):
    #     db = next(get_db())
    # # def __init__(self, db: Session, model,
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
    def get_all(self, db: Session, with_trash: bool = False):
        query = db.query(self._model)
        if not with_trash:
            query = query.filter(self._model.deleted_at.is_(None))
        print(query.all())
        return query.all()

    @abstractmethod
    def paginate(self, db: Session, params_pagination, params=None, with_trash: bool = False):
        try:
            query = db.query(self._model)
            if params:
                for key, param in params:
                    if param:
                        if type(param) is int:
                            query = query.filter(getattr(self._model, key) == param)
                        else:
                            query = query.filter(getattr(self._model, key).ilike(f'%{param}%'))
            if hasattr(params_pagination, 'except_ids') and params_pagination.except_ids:
                except_ids = params_pagination.except_ids.split(',')
                query = query.filter(self._model.id.not_in(except_ids))
            if hasattr(params_pagination, 'exist_ids') and params_pagination.exist_ids:
                exist_ids = params_pagination.exist_ids.split(',')
                query = query.filter(self._model.id.in_(exist_ids))
            # if len(params) > 0:
            #     for key, value in params.items():
            #         print(key, value)
            if not with_trash:
                query = query.filter(self._model.deleted_at.is_(None))
            data = paginate(self._model, query, params_pagination)

            return data
        except:
            db.rollback()
            raise

    @abstractmethod
    def find(self, db: Session, id: int, with_trash: bool = False):
        query = db.query(self._model).filter(self._model.id == id)

        if not with_trash:
            query = query.filter(self._model.deleted_at.is_(None))

        obj = query.first()

        # if not obj:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object with the id: {id} is not available")
        return obj

    @abstractmethod
    def get_by_user_id(self, db: Session, user_id, is_get_first: bool = False, is_primary: bool = False, with_trash: bool = False, order='asc'):
        direction = desc if order == 'desc' else asc
        query = db.query(self._model).filter(self._model.user_id == user_id).order_by(direction('created_at'))

        if is_primary:
            query = query.filter(self._model.is_primary)

        if not with_trash:
            query = query.filter(self._model.deleted_at.is_(None))

        if not is_get_first:
            obj = query.all()
        else:
            obj = query.first()

        # if not obj:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object with the user_id: {user_id} is not available")
        return obj

    @abstractmethod
    def search(self, db: Session, fields: dict = {}, is_absolute: bool = False, is_get_first = True):
        query = db.query(self._model)
        if fields:
            for k, v in fields.items():
                if v:
                    if type(v) == int:
                        query = query.filter(getattr(self._model, k) == v)
                    else:
                        v = v.strip()
                        if is_absolute:
                            query = query.filter(getattr(self._model, k).ilike(f'{v}'))
                        else:
                            query = query.filter(getattr(self._model, k).ilike(f'%{v}%'))
        if is_get_first:
            return query.first()
        # if not obj:
        #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail=f"Object is not available")
        return query.all()

    @abstractmethod
    def create(self, db: Session, data):
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
            db.commit()
            db.refresh(data)
            return data
        except:
            db.rollback()
            raise

    @abstractmethod
    def update(self, db: Session, id, data, with_restore: bool = False):

        q_obj = db.query(self._model).filter(self._model.id == id)
        if not q_obj.first():
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
            # obj = q_obj.first()
            # for k, v in data.items():
            #     setattr(obj, k, v)
            # obj = obj(**data)
            # db.add(obj)
            q_obj.update(data)
            # db.flush()
            db.commit()
            # db.refresh(obj)
            return q_obj.first()

        except Exception as e:
            print(e)
            db.rollback()
            raise

    @abstractmethod
    def delete(self, db: Session, id, is_hard_delete: bool = False):
        obj = db.query(self._model).filter(self._model.id == id)
        if not obj.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Object with the id: {id} is not available")

        if not is_hard_delete:
            if hasattr(self._model, 'deleted_at') and str(self._model.deleted_at.type) == 'INTEGER':
                current_time = helper.get_current_time_as_int()
            else:
                current_time = func.now()
            obj.update({'deleted_at': current_time})
        else:
            obj.delete()
        db.commit()
        # db.refresh(obj)

        return obj.first()
