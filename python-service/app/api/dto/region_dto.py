from typing import Optional

from pydantic import BaseModel

from app.data.domains.contacts import Contacts


class RegionDto(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    is_main: bool
    contacts: Contacts
    admin: Optional["UserDto"] = None

from app.api.dto.user_dto import UserDto
RegionDto.model_rebuild()