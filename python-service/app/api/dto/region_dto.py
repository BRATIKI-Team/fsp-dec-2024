from typing import Optional

from pydantic import BaseModel

from app.data.domains.contacts import Contacts


class RegionDto(BaseModel):
    id: Optional[str] = None
    name: str
    subject: str
    description: Optional[str]
    is_main: bool
    contacts: Contacts
    admin: Optional["UserDto"] = None


class RegionCreateReq(BaseModel):
    name: str
    subject: str
    is_main: bool


from app.api.dto.user_dto import UserDto

RegionDto.model_rebuild()
