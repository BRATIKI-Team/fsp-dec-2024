from datetime import datetime
from typing import Annotated

from bson import Binary
from fastapi import Depends, UploadFile

from app.core.dependencies import transliterate
from app.data.domains.file_model import FileModel
from app.data.repositories.file_model_repository import FileRepository
from app.services.base_service import BaseService


class FileModelService(BaseService[FileModel]):
    def __init__(
            self,
            file_repository: Annotated[FileRepository, Depends(FileRepository)]
    ):
        super().__init__(file_repository)
        self._file_repository = file_repository

    async def upload_file(self, file: UploadFile) -> str:
        file_content = await file.read()
        upload_file = FileModel(
            file_name=file.filename,
            file_data=Binary(file_content),
            file_type=file.content_type,
            uploaded_at=datetime.now()
        )

        return await self._file_repository.insert(upload_file)