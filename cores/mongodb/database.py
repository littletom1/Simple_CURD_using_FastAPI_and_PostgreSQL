import motor.motor_asyncio
from settings import (
MONGODB_USERNAME,
MONGODB_PASSWORD,
MONGODB_HOST,
MONGODB_PORT,
MONGODB_DATABASE,
MONGODB_AUTHENTICATION_DATABASE,
)
mongouri = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}?authSource={MONGODB_AUTHENTICATION_DATABASE}'
client = motor.motor_asyncio.AsyncIOMotorClient(mongouri)
database = getattr(client, MONGODB_DATABASE)
