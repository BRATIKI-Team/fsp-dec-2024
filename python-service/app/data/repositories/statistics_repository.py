from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.statistics import Statistics
from app.data.repositories.base_repository import BaseRepository, T


class StatisticsRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "statistics")

    def serialize(self, document: Dict) -> T:
        return Statistics(**document)
