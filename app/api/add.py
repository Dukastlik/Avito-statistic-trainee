import requests
from fastapi import HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from models.QStat import Timestamp, QStat
from db.db_operations import add_query_stat
from db.mongodb import db, DataBase


KEY = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
AVITO_URI = "https://www.avito.ru/"


async def get_location_id(region: str) -> str:

    # Retrieving locationid through Avito api

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
            return location_id
    if location_id == "":
        raise HTTPException(
            status_code=400,
            detail="Enter valid region name",
        )


async def get_query_info(query: str, region: str) -> dict:

    # Retrieving query info through Avito api

    # getting location id
    location_id = await get_location_id(region)
    # getting number of ads for query-region pair and top 4 ad info
    resp = requests.get(
            "https://m.avito.ru/api/9/items",
            params={
                "key": KEY,
                "query": query,
                "locationId": location_id
            }
        )
    json_response = resp.json()
    ad_count = json_response['result']['mainCount']
    # top 4 ad information
    top_ads = []
    for i in range(4):
        item = json_response['result']['items'][i]
        top_ad_uri = AVITO_URI + item['value']['uri_mweb']
        top_ad_title = item['value']['title']
        top_ads.append({'ad_title': top_ad_title, 'ad_uri': top_ad_uri})
    ad_info = {'ad_count': ad_count, 'top_ads': top_ads}
    return ad_info



async def create_new_stat(query: str, region: str, ad_info: dict):

    #Creating a QStat object
    #for query-region pair to insert in db

    # unpacking ad_info
    ad_count = ad_info["ad_count"]
    top_ads = ad_info["top_ads"]
    # current datetime in POSIX timestamp
    current_time = datetime.now().timestamp()
    # creating timestamp object
    newtimestamp = Timestamp(
        timestamp=current_time,
        ad_count=ad_count,
        top_ads=top_ads
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
    # getting query info
    ad_info = await get_query_info(query, region)
    # creating new stat to insert
    new_qstat = await create_new_stat(query, region, ad_info)
    # inserting new entity to db
    new_query_id = await add_query_stat(db.client, new_qstat.dict(by_alias=True))
    return new_query_id
