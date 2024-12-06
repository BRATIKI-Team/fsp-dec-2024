from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Event(BaseModel):
    id: Optional[str] = None
    regionId: str
    name: str
    discipline: str
    description: str
    datetime: datetime