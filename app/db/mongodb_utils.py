from motor.motor_asyncio import AsyncIOMotorClient
from db.mongodb import db


MONGO_DETAILS = "mongodb:27017"
DB_NAME = "AvitoStat"
COLLECTION = "query_stat"


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(MONGO_DETAILS)


async def close_mongo_connection():
    db.client.close()
