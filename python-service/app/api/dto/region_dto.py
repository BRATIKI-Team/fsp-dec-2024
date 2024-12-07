from typing import Optional

from pydantic import BaseModel

from app.data.domains.contacts import Contacts


class RegionDto(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    isMain: bool
    contacts: Contacts
    admin: "UserDto"

from app.api.dto.user_dto import UserDto
RegionDto.model_rebuild()