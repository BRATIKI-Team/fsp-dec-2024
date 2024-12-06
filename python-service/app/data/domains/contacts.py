from typing import List

from pydantic import BaseModel


class Contacts(BaseModel):
    email: str
    phone: str
    social_links: List[str]