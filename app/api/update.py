from asyncio import sleep
from datetime import datetime
from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClient
from api.add import get_query_info
from models.QStat import Timestamp
from db.db_operations import update_query_stat, get_all_stats
from db.mongodb import db, DataBase


UPDATE_RATE = 60


async def update_query(
        qid: str,
        query: str,
        region: str,
        background_tasks: BackgroundTasks,
        delay=UPDATE_RATE,
        db: DataBase = db,
):
    await sleep(delay)
    # getting new count of ads
    new_query_info = await get_query_info(query, region)
    new_ad_count = new_query_info["ad_count"]
    new_top_ads = new_query_info["top_ads"]
    # current datetime in POSIX timestamp
    current_time = datetime.now().timestamp()
    # creating new timestamp
    new_time_stamp = Timestamp(
                timestamp=current_time,
                ad_count=new_ad_count,
                top_ads=new_top_ads
    )
    # inserting new timestamp to database
    stat_updated = await update_query_stat(db.client, qid, new_time_stamp.dict())
    background_tasks.add_task(update_query, qid, query, region, background_tasks)
    return stat_updated


async def update_on_startup(background_tasks: BackgroundTasks):
    stats = await get_all_stats()
    print(stats)
    '''current_time = datetime.now().timestamp()
    for item in stats:
        dt = current_time - item["stat"][0]["timestamp"]
        if 0 < dt < UPDATE_RATE:
            
'''
