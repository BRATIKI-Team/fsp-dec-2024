from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from app.data.domains.team_result import TeamResult


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
    documents_ids: Optional[List[str]] = None
    protocols_ids: Optional[List[str]] = None
    teams_results: Optional[List[TeamResult]] = None
    is_approved_event: bool


class EventFilter(str, Enum):
    regions = 'regions'
    disciplines = 'disciplines'
