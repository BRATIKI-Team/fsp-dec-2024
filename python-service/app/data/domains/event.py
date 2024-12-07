from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class Event(BaseModel):
    id: Optional[str] = None
    region_id: str
    name: str
    location: str
    participants_count: int
    start_date: datetime
    end_date: datetime
    member_created_id: Optional[str] = None
    discipline: Optional[str] = None
    description: Optional[str] = None
    documents_ids: List[str] = []
    protocols_ids: List[str] = []
    is_approved_event: bool

class EventFilter(str, Enum):
    regions = 'regions'
    disciplines = 'disciplines'
