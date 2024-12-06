from typing import Optional

from pydantic import BaseModel

from app.data.domains.contacts import Contacts


class Region(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    isMain: bool
    contacts: Contacts