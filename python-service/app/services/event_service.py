from typing import Annotated

from fastapi import Depends

from app.data.domains.event_request import EventRequest, EventStatus
from app.data.domains.user import User
from app.data.repositories.event_repository import EventRepository
from app.data.repositories.event_request_repository import EventRequestRepository
from app.services.base_service import BaseService

class EventService(BaseService[User]):
    def __init__(
            self,
            event_repository: Annotated[EventRepository, Depends(EventRepository)],
            event_request_repository: Annotated[EventRequestRepository, Depends(EventRequestRepository)]):
        super().__init__(event_repository)
        self.event_repository = event_repository
        self.event_request_repository = event_request_repository


    async def create_request_for_event(self, event_id: str) -> bool:
        event = await self.event_repository.get(event_id)
        if event is None:
            raise Exception("Event is not found")
        event_request = EventRequest(
            event_id = event.id,
            status = EventStatus.PENDING
        )
        event_request_id = await self.event_request_repository.insert(event_request)
        return event_request_id is not None
