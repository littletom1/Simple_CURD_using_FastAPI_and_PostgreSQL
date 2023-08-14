# from sqlalchemy.pool import NullPool
# from sqlalchemy.orm import sessionmaker
# from decouple import config
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import AsyncSession
# _host = config('db_host')
# _username = config('db_username')
# _password = config('db_password')
# _database = config('db_database')


# # async def get_db() -> AsyncSession:
# #     async with async_session() as session:
# #         try:
# #             yield session
# #         finally:
# #             await session.close()
# async def get_db() -> AsyncSession:
#     _engine = create_async_engine(
#         f'mysql+asyncmy://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool,
#         isolation_level="READ UNCOMMITTED")
#     async_session = sessionmaker(autocommit=False, autoflush=False, bind=_engine, class_=AsyncSession, expire_on_commit=False)
#     async with async_session() as session:
#         try:
#             yield session
#         finally:
#             await session.close()