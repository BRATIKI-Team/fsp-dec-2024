from enum import Enum
from typing import Optional

from pydantic import BaseModel

class EventStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    CANCELED = "canceled"

class EventRequest(BaseModel):
    id: Optional[str] = None
    event_id: str
    status: EventStatus
    canceled_reason: Optional[str] = None
