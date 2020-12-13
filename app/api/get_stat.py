from datetime import datetime
from db.db_operations import get_query_stat
from db.mongodb import db, DataBase



async def get_stat(
        qid: str, start_time: str, end_time: str, db: DataBase = db
):
    # TODO error Response
    # converting time to POSIX timestamp
    posix_start_time = datetime.strptime(start_time, "%Y-%m-%d-%H").timestamp()
    posix_end_time = datetime.strptime(end_time, "%Y-%m-%d-%H").timestamp()

    query_stat = await get_query_stat(db.client, qid, posix_start_time, posix_end_time)
    response = {}
    for item in query_stat[0]["stat"]:
        timestamp = datetime.fromtimestamp(item["timestamp"])
        ad_count = item["ad_count"]
        top_ads = item["top_ads"]
        response[timestamp] = {"ad count": ad_count, "top ads": top_ads}
    return response

