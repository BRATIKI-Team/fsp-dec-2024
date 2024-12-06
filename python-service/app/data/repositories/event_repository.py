from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.dto import SearchReq, Page
from app.core.dependencies import get_db
from app.data.domains.event import Event
from app.data.repositories.base_repository import BaseRepository
from app.data.repositories.event_filter_repository import EventFilterRepository


class EventRepository(BaseRepository):
    def __init__(
            self,
            db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
            event_filter_repository: Annotated[EventFilterRepository, Depends(EventFilterRepository)]
    ):
        super().__init__(db, "events")
        self._event_filter_repository = event_filter_repository

    def serialize(self, document: Dict) -> Event:
        return Event(**document)

    async def search(self, req: SearchReq) -> Page[Event]:
        return await self.paginate(
            cursor=self._event_filter_repository.apply(self.collection, req=req),
            req=req
        )
