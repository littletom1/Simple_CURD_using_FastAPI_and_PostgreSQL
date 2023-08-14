from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from typing import Any
from cores.helpers.paging import Page, PaginationParams
from cores.schemas.sche_base import DataResponse
from cores.postgresql.connection import get_db
from sqlalchemy.orm import Session
from v1.schemas.post_schema import CreatePostSchema, UpdatePostSchema, PostResponse
from db.models.Post import Post
from data_providers.posts.post_concrete import PostConcrete
from cores.postgresql.service_base import ServiceBase

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/post',
    tags=['POSTS'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)
service = ServiceBase()
model = Post

@router.get('/{id}')
def get_post(id: str, db: Session = Depends(get_db)):
    data = service.find(id=id,model=model)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")
    return DataResponse().success_response(data=data)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(post: CreatePostSchema, db: Session = Depends(get_db)):
    data = service.create(data=post, model=model)
    return DataResponse().success_response(data=data)

@router.get('/',status_code=status.HTTP_201_CREATED)
def get_all(db: Session = Depends(get_db)):
    data = service.get_all(model=model)
    return DataResponse().success_response(data=data)

@router.put('/{id}',status_code=status.HTTP_201_CREATED)
def update(id:str,post: UpdatePostSchema,db: Session = Depends(get_db)):
    data = service.update(id,post,model)
    return DataResponse().success_response(data=data)

@router.delete('/{id}',status_code=status.HTTP_201_CREATED)
def delete(id:str,db: Session = Depends(get_db)):
    data = service.delete(id, model)
    return DataResponse().success_response(data=data)

@router.get('/panigate/',status_code=status.HTTP_201_CREATED)
def panigate(params: PaginationParams = Depends(),db: Session = Depends(get_db)):
    data = service.paginate(params, model)
    return DataResponse().success_response(data=data)