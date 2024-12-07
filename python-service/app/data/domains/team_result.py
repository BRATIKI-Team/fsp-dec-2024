from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TeamPlace(str, Enum):
    FIRST = "first",
    SECOND = "second",
    THIRD = "third"

class TeamResult(BaseModel):
    id: Optional[str] = None
    name: str
    region_id: str
    place: Optional[TeamPlace] = None