from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    id: Optional[str] = None
    region_id: str
    name: str
    datetime: datetime
    member_created_id: Optional[str] = None
    discipline: Optional[str] = None
    description: Optional[str] = None
    is_approved_event: bool


class EventFilter(str, Enum):
    regions = 'regions'
    disciplines = 'disciplines'
