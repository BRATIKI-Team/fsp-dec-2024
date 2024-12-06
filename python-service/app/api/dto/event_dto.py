from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.data.domains.event import Event
from app.data.domains.region import Region
from app.data.domains.user import User


class CreateEventReq(BaseModel):
    name: str
    discipline: str
    description: str
    datetime: datetime

class ExtendedEvent(BaseModel):
    event: Event
    region: Optional[Region]
    user: Optional[User]