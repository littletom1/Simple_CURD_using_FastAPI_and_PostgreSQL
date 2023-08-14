from decouple import config
class PostConcrete():
    def __init__(self):
        if config('POST_PROVIDER') == 'database':
            from services.db_services.post_service import PostService
            self.service = PostService()