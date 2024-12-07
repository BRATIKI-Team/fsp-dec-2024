from typing import Optional

from pydantic import BaseModel

from app.data.domains.contacts import Contacts


class Region(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    person: Optional[str]
    is_main: bool
    contacts: Optional[Contacts]
    admin_id: Optional[str] = None