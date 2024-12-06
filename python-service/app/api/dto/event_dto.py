from datetime import datetime

from pydantic import BaseModel


class CreateEventReq(BaseModel):
    name: str
    discipline: str
    description: str
    datetime: datetime