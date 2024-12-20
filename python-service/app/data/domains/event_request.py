from enum import Enum
from typing import Optional

from pydantic import BaseModel

class EventRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class EventRequest(BaseModel):
    id: Optional[str] = None
    event_id: str
    region_id: str
    status: EventRequestStatus
    canceled_reason: Optional[str] = None