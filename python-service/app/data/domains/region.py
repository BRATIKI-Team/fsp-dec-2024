from typing import Optional

from pydantic import BaseModel


class Region(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    isMain: bool