from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.api.dto.file_model_dto import FileModelDto
from app.data.domains.event import Event
from app.data.domains.event_request import EventRequest
from app.data.domains.region import Region
from app.data.domains.user import User


class CreateEventReq(BaseModel):
    name: str
    discipline: str
    description: str
    location: str
    participants_count: int
    start_date: datetime
    end_date: datetime
    documents_ids: List[str]
    protocols_ids: List[str]


class ExtendedEvent(BaseModel):
    event: Event
    region: Optional[Region]
    user: Optional[User]
    documents: List[FileModelDto]
    protocols: List[FileModelDto]
    request: Optional[EventRequest]
