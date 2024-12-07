from typing import Optional

from pydantic import BaseModel, EmailStr

from app.api.dto.region_dto import RegionDto
from app.data.domains.user import UserRole


class UserDto(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    role: UserRole
    region: Optional[RegionDto] = None