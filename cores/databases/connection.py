# from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
# from sqlalchemy.orm import sessionmaker
# from decouple import config
# from sqlalchemy.orm import Session
# from typing import Generator
# _host = config('db_host')
# _username = config('db_username')
# _password = config('db_password')
# _database = config('db_database')
# # _database = 'test_competition_vote_service'


# _engine = create_engine(
#     f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
# Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

# def get_db() -> Generator:
#     db: Session = Session_Local()
#     try:
#         yield db
#     finally:
#         db.close()

