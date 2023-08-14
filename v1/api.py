from fastapi import FastAPI, APIRouter, Request, Depends
# from cores.elasticsearch.es_helper import ElasticSearch
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from v1.di import init_di
from cores.postgresql.connection import get_db
from v1.routers import post
from sqlalchemy.orm import Session
# from enums.db import table_enum
import json

# # from starlette.middleware import Middleware
#
# desc = """
# # Api For School Service
# # """
tags_metadata = [
    {
        "name": "Simple CURD",
        "description": "simple api for testing curd with postgreSQL",
    },
    {
        "name": "POSTS",
        "description": "posts test connection"
    }

]

app = FastAPI(
    title='API For Testing',
    # description=desc,
    version='1',
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url="/redoc")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_di()

app.include_router(post.router)

router = APIRouter(
    prefix="/utils",
    tags=["utilities"]
)
from decouple import config
from sqlalchemy import create_engine
from db import Base
@router.get('/create_tables')
def create_tables(password: str):
    if password == 'password123':
        engine = create_engine(
            f"postgresql://{config('db_username')}:{config('db_password')}@{config('db_host')}:{config('DB_PORT')}/{config('db_database')}")
        Base.metadata.create_all(engine)
        return 'OK'
    else: 
        return 'No'
    
app.include_router(router)

