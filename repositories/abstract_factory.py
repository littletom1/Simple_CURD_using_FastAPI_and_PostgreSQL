from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import DBHelper
class AbstractFactory(ABC):
    @abstractmethod
    def create(self, obj):
        db = DBHelper().get_db()
        db.add(obj)
        db.commit()
        db.refresh(obj)
        db.close()
        return obj
    # @abstractmethod
    # def get_elastic(self):
    #     pass