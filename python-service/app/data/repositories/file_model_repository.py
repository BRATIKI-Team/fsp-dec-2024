from typing import Annotated, Dict

from bson import Binary
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.file_model import FileModel
from app.data.repositories.base_repository import BaseRepository


class FileRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "files")

    def serialize(self, document: Dict) -> FileModel:
        document["file_data"] = Binary(document["file_data"])
        print(document["file_data"])
        return FileModel(**document)