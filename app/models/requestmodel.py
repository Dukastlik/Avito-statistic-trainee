from pydantic import BaseModel
from fastapi import Query


class AddRequest(BaseModel):
    query: str
    region: str


class StatRequest(BaseModel):
    id: str = Query(..., min_length=24, max_length=24)
    start_time: str
    end_time: str
