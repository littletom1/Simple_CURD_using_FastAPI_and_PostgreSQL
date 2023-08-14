from pythondi import inject
from sqlalchemy.orm import Session
from repositories.contracts.post_contract import PostContract
from data_providers.posts.post_layer_contract import PostLayerContract
import json

class PostService(PostLayerContract):
    @inject()
    def __init__(self, repo: PostContract):
        self.repo = repo

    # def find(self, db, id):
    #     pass

    # def paginate(self, db):
    #     pass
    
    # def create(self, db, obj):
    #     pass
    
    #function to query will be write here
