from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.event_request import EventRequest
from app.data.repositories.base_repository import BaseRepository, T


class EventRequestRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "event-requests")

    def serialize(self, document: Dict) -> T:
        return EventRequest(**document)
