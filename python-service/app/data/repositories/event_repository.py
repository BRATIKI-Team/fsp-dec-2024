from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependecies import get_db
from app.data.domains.event import Event
from app.data.repositories.base_repository import BaseRepository, T


class EventRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "events")

    def serialize(self, document: Dict) -> T:
        return Event(**document)