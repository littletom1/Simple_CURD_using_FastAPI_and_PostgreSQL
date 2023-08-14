from pythondi import Provider, configure
from repositories.contracts.post_contract import PostContract
from repositories.sqlachemy.post_repository import PostRepository

"""
    Khỏi tạo dependency injection
    Quyết định class nào sẽ được thực thi khi implement từ interface
"""
def init_di():
    provider = Provider()
    provider.bind(PostContract, PostRepository)
    configure(provider=provider)

    