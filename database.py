from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.seriesbot


def get_series_collection():
    return db.series


def get_user_collection():
    return db.users
