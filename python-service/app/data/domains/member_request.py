from enum import Enum
from typing import Optional

from pydantic import BaseModel

class MemberRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"

class MemberRequest(BaseModel):
    id: Optional[str] = None
    region_id: str
    user_id: str
    status: MemberRequestStatus