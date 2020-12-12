from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AddRequest(BaseModel):
    query: str
    region: str


class StatRequest(BaseModel):
    id: str
    start_time: str
    end_time: str