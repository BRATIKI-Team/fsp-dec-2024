from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FileModel(BaseModel):
    id: Optional[str] = None
    file_name: str
    file_data: bytes
    file_type: str
    uploaded_at: datetime = datetime.now()