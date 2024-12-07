from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class FileModelDto(BaseModel):
    id: Optional[str] = None
    file_name: str
    file_type: str
    upload_at: datetime