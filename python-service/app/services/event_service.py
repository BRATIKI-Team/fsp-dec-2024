from datetime import datetime
from typing import Annotated
from venv import create

from fastapi import Depends

from app.api.dto.event_dto import CreateEventReq
from app.data.domains.event import Event
from app.data.domains.event_request import EventRequest, EventStatus
from app.data.domains.user import User
from app.data.repositories.event_repository import EventRepository
from app.data.repositories.event_request_repository import EventRequestRepository
from app.data.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.services.user_service import UserService


class EventService(BaseService[User]):
    def __init__(
            self,
            user_service:Annotated[UserService, Depends(UserService)],
            event_repository: Annotated[EventRepository, Depends(EventRepository)],
            event_request_repository: Annotated[EventRequestRepository, Depends(EventRequestRepository)]):
        super().__init__(event_repository)
        self._user_service = user_service
        self._event_repository = event_repository
        self._event_request_repository = event_request_repository


    async def create_event(self, user_id: str, create_event_dto: CreateEventReq) -> bool:
        user = await self._user_service.get(user_id)
        # if user.region_id is None:
        #     raise Exception("Has no permission")
        region_id = "6752f8b0f03f50dc0e8f5244"
        event = Event(
            region_id=region_id,
            name=create_event_dto.name,
            discipline=create_event_dto.discipline,
            description=create_event_dto.description,
            datetime=create_event_dto.datetime
        )
        event_id = await super().create(event)
        return event_id is not None

    async def create_request_for_event(self, event_id: str) -> bool:
        event = await self._event_repository.get(event_id)
        if event is None:
            raise Exception("Event is not found")
        event_request = EventRequest(
            event_id = event.id,
            status = EventStatus.PENDING
        )
        event_request_id = await self._event_request_repository.insert(event_request)
        return event_request_id is not None
