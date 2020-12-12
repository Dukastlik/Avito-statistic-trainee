import requests
from fastapi import HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from models.QStat import Timestamp, QStat
from db.db_operations import add_query_stat
from db.mongodb import db, DataBase


KEY = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'


async def get_ad_count(query: str, region: str) -> int:
    '''
    Retrieving ads count through Avito api
    '''
    # getting location id
    location_id = ""
    resp = requests.get(
            "https://m.avito.ru/api/1/slocations",
            params={
                "key": KEY,
                "q": region
            }
        )
    counties_list = resp.json()["result"]["locations"]
    for item in counties_list:
        if item["names"]["1"] == region:
            location_id = item["id"]
            break

    if location_id == "":
        raise HTTPException(
            status_code=400,
            detail="Enter valid region name",
        )
    # getting number of ads for query-region pair
    resp = requests.get(
            "https://m.avito.ru/api/9/items",
            params={
                "key": KEY,
                "query": query,
                "locationId": location_id
            }
        )
    ad_count = resp.json()['result']['mainCount']
    return ad_count


async def create_new_stat(query: str, region: str, ad_count: int):
    '''
    Creating a QStat object
    for query-region pair to insert in db
    '''
    # current datetime in POSIX timestamp
    current_time = datetime.now().timestamp()
    # creating timestamp object
    newtimestamp = Timestamp(
        timestamp=current_time,
        ad_count=ad_count
    )
    # creating statistic object
    new_qstat = QStat(
        _id=ObjectId(),
        query=query,
        region=region,
        stat=[newtimestamp, ]
    )
    return new_qstat


async def register_new_query(
        query: str, region: str, db: DataBase = db
):
    '''
    Add new query region pair to db
    '''
    # getting ad count
    ad_count = await get_ad_count(query, region)
    # creating new stat to insert
    new_qstat = await create_new_stat(query, region, ad_count)
    # inserting new entity to db
    new_query_id = await add_query_stat(db.client, new_qstat.dict(by_alias=True))
    return new_query_id
