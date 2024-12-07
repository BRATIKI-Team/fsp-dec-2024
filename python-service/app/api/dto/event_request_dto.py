from typing import Optional

from pydantic import BaseModel

from app.data.domains.event import Event
from app.data.domains.event_request import EventRequestStatus
from app.data.domains.region import Region


class EventRequestDto(BaseModel):
    id: Optional[str] = None
    event_id: str
    region_id: str
    status: EventRequestStatus
    canceled_reason: Optional[str] = None
    region: Region
    event: Event
class SendEventRequestResult(BaseModel):
    error: Optional[str] = None