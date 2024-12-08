from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TeamPlace(str, Enum):
    FIRST = "first",
    SECOND = "second",
    THIRD = "third"

class TeamResult(BaseModel):
    name: str
    region_id: str
    rating: int
    place: Optional[TeamPlace] = None