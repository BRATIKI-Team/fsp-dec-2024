from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.api.dto.file_model_dto import FileModelDto


class FileModel(BaseModel):
    id: Optional[str] = None
    file_name: str
    file_data: bytes
    file_type: str
    uploaded_at: datetime = datetime.now()

    def get_dto(self) -> FileModelDto:
        return FileModelDto(
            id=self.id,
            file_name=self.file_name,
            file_type=self.file_type,
            upload_at=self.uploaded_at
        )
