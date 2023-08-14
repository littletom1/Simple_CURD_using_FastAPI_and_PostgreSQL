# from sqlalchemy_utils import database_exists, create_database, drop_database
# def create_db(self):
#     if database_exists(self._engine.url):
#         drop_database(self._engine.url)

#     create_database(self._engine.url, encoding='utf8mb4')
#     self._engine.dispose(close=True)
#     return database_exists(self._engine.url)