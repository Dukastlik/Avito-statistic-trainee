from pydantic import BaseModel, Field
from bson import ObjectId
import datetime
from typing import List, Optional


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


'''class TopAdd(BaseModel):
    ad_title: str
    ad_url: str'''


class Timestamp(BaseModel):
    timestamp: float
    ad_count: int
    top_ads: List[dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class QStat(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    query: str
    region: str
    stat: List[Timestamp]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }



