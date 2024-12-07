from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.statistics_file import StatisticsFile
from app.data.repositories.base_repository import BaseRepository, T


class StatisticsFileRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "statistics_files")

    def serialize(self, document: Dict) -> T:
        return StatisticsFile(**document)