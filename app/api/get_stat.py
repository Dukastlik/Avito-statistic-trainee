from datetime import datetime
from fastapi import HTTPException
from db.db_operations import get_query_stat
from db.mongodb import db, DataBase


async def get_stat(
        qid: str, start_time: str, end_time: str, db: DataBase = db
) -> dict:

    # converting time to POSIX timestamp
    try:
        posix_start_time = datetime.strptime(start_time, "%Y-%m-%d-%H").timestamp()
        posix_end_time = datetime.strptime(end_time, "%Y-%m-%d-%H").timestamp()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Date-Time format invalid"
        )

    # getting statistic for query/time period from db
    query_stat = await get_query_stat(db.client, qid, posix_start_time, posix_end_time)
    if query_stat == []:
        raise HTTPException(
            status_code=400,
            detail="Stat with id {0} not found".format(qid),
        )

    # forming a response from db data
    response = {}
    for item in query_stat[0]["stat"]:
        timestamp = datetime.fromtimestamp(item["timestamp"])
        ad_count = item["ad_count"]
        top_ads = item["top_ads"]
        if timestamp not in response:
            response[timestamp] = {"ad count": ad_count, "top ads": top_ads}
    return response
