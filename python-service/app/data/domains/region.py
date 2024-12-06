from typing import Optional

from pydantic.v1 import BaseModel


class Region(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    isMain: bool