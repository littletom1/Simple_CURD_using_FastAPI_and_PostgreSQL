# from db import Base
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from .connection import Session_Local, _engine
# from typing import Generator
# def create_table():
#     Base.metadata.create_all(_engine)
#     return True

# def store(obj):
#     session = Session_Local()
#     session.add(obj)
#     session.commit()
#     session.close()
#     return obj
