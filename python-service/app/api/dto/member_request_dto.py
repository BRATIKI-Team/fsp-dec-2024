from typing import Optional

from pydantic import BaseModel

from app.api.dto.user_dto import UserDto
from app.data.domains.member_request import MemberRequestStatus


class SendMemberRequestResult(BaseModel):
    error: Optional[str] = None


class ExtendedMemberRequest(BaseModel):
    id: Optional[str] = None
    region_id: str
    user: UserDto
    status: MemberRequestStatus
