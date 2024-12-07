import base64
from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.file_model import FileModel
from app.data.repositories.base_repository import BaseRepository, T


class FileRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "files")

    def serialize(self, document: Dict) -> FileModel:
        document["file_data"] = base64.b64encode(document["file_data"]).decode('utf-8')
        return FileModel(**document)