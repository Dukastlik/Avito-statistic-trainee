from motor.motor_asyncio import AsyncIOMotorClient
from models.QStat import QStat
from bson.objectid import ObjectId
from db.mongodb_utils import DB_NAME, COLLECTION
from db.mongodb import db


async def add_query_stat(
        conn: AsyncIOMotorClient, querydata: QStat
) -> int:
    query = await conn[DB_NAME][COLLECTION].insert_one(querydata)
    return query.inserted_id


async def get_query_stat(
        conn: AsyncIOMotorClient, qid: str, start_time: float, end_time: float
) -> list:
    pipeline = [
        {"$match": {"_id": ObjectId(qid)}},
        {"$unwind": "$stat"},
        {"$match": {"stat.timestamp": {"$gte": start_time, "$lte": end_time}}},
        {"$group": {"_id": "$_id", "stat": {"$push": "$stat"}}},
        {"$project": {"_id": 0, "stat": 1}}
    ]
    stat = conn[DB_NAME][COLLECTION].aggregate(pipeline)
    if stat:
        stat_list = await stat.to_list(length=1000)
        return stat_list


async def update_query_stat(
        conn: AsyncIOMotorClient, qid: str, data: dict
) -> bool:
    querystat = await conn[DB_NAME][COLLECTION].find_one({"_id": ObjectId(qid)})
    if querystat:
        updated_query = await conn[DB_NAME][COLLECTION].update_one(
            {"_id": ObjectId(qid)},
            {"$push": {"stat": data}}
        )
        if updated_query:
            return True
        return False


async def get_last_stats() -> list:

    conn = db.client
    all_stats = conn[DB_NAME][COLLECTION].find({}, {"stat": {"$slice": -1}})
    if all_stats:
        stat_list = await all_stats.to_list(length=1000)
        return stat_list
