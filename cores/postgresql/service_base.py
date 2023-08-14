from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .service_base_contract import ServiceBaseContract
from cores.schemas.sche_base import PaginationParams, MetadataSchema
from decouple import config
from datetime import datetime
POSTGRESQL_URI=f"postgresql://{config('db_username')}:{config('db_password')}@{config('db_host')}:{config('DB_PORT')}/{config('db_database')}"

class ServiceBase(ServiceBaseContract):
    def __init__(self):
        self.engine = create_engine(POSTGRESQL_URI)
        self.Session = sessionmaker(bind=self.engine)

    # def convert_data(self, data):
    #     if data:
    #         data['id'] = str(data['id'])
    #     return data

    def paginate(self, pagination_params,model:type, query:dict = {}, with_trash: bool = False, sort_by:dict = None, direction = None):
        page = pagination_params.page
        size = pagination_params.page_size
        objs = []
        session = self.Session()
        q = session.query(model)
        if pagination_params.sort_by and pagination_params.order:
            sort_column = getattr(model, pagination_params.sort_by, None)
            if sort_column is not None:
                if pagination_params.order == "asc":
                    q = q.order_by(sort_column)
                elif pagination_params.order == "desc":
                    q = q.order_by(sort_column.desc())
        total = q.count()
        objs = q.offset(size * (page - 1)).limit(size).all()
        session.close()
        metadata = MetadataSchema(
            current_page=page,
            page_size=size,
            total_items=total
        )
        return {
            'code': 200,
            'data': objs,
            'metadata': metadata
        }

    def get_all(self, model:type):
        objs = []
        session = self.Session()
        objs = session.query(model).all()
        session.close()
        return objs

    def create(self, data: object, model: type, with_timestamp = True) -> dict:
        session = self.Session()
        obj = model(**data.dict())
        if with_timestamp:
            obj.created_at = obj.updated_at = datetime.now()
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj

    def find(self, id:str, model:type) -> dict:
        session = self.Session()
        obj = session.query(model).filter_by(id=id).first()
        session.close()
        return obj

    def search(self, name:str,model:type, is_absolute:bool = True, is_get_first:bool = True):
        session = self.Session()
        q = session.query(model)
        if is_get_first:
            if is_absolute:
                obj = q.filter_by(name=name).first()
                session.close()
                return self.convert_data(obj)
            else:
                objs = q.filter(model.name.ilike(f'%{name}%')).all()
                session.close()
                return [self.convert_data(obj) for obj in objs]
        else:
            if is_absolute:
                objs = q.filter_by(name=name).all()
                session.close()
                return [self.convert_data(obj) for obj in objs]
            else:
                objs = q.filter(model.name.ilike(f'%{name}%')).all()
                session.close()
                return [self.convert_data(obj) for obj in objs]

    def update(self, id:str, data: object,model:type) -> dict:
        session = self.Session()
        obj = session.query(model).filter_by(id=id).first()
        if obj:
            data_dict = data.dict()
            for key, value in data_dict.items():
                setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            session.close()
            return obj
        session.close()
        return False

    def delete(self, id: str, model: type, is_hard_delete: bool = True) -> bool:
        session = self.Session()
        obj = session.query(model).filter_by(id=id).first()
        if obj:
            if is_hard_delete:
                session.delete(obj)
                session.commit()
            else:
                obj.deleted_at = datetime.now()
                session.commit()
            session.close()
            return True
        session.close()
        return False