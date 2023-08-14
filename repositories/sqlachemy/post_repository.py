from cores.repositories.abstracts.sqlachemy_abstract import SqlAchemyAbstract
from db import Post
from sqlalchemy.orm import Session
from repositories.contracts.post_contract import PostContract
class PostRepository(SqlAchemyAbstract, PostContract):
    def __init__(self):
        self.set_model(Post)
        super().__init__()

    def get_by(self, db, user_id):
        return user_id
