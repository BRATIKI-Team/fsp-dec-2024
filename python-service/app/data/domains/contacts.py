from typing import List, Optional

from pydantic import BaseModel


class Contacts(BaseModel):
    email: str = ""
    phone: Optional[str] = None
    social_links: Optional[List[str]] = None