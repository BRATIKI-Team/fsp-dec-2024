from typing import Annotated

from fastapi import Depends

from app.data.domains.event_request import EventRequest, EventRequestStatus
from app.data.repositories.event_request_repository import EventRequestRepository
from app.services.base_service import BaseService
from app.services.event_service import EventService
from app.services.user_service import UserService


class EventRequestService(BaseService[EventRequest]):
    def __init__(
            self,
            user_service:Annotated[UserService, Depends(UserService)],
            event_service: Annotated[EventService, Depends(EventService)],
            event_request_repository: Annotated[EventRequestRepository, Depends(EventRequestRepository)]):
        super().__init__(event_request_repository)
        self._user_service = user_service
        self._event_service = event_service
        self._event_request_repository = event_request_repository

    async def update_status(self, request_id: str, event_request: EventRequest) -> bool:
        event = await self._event_service.get(event_request.event_id)
        if event is None:
            raise Exception("Event is not found")

        return await super().update(request_id, event_request)
        # todo: send email notification to user that sent request

    async def create_request_for_event(self, event_id: str) -> bool:
        event = await self._event_service.get(event_id)
        if event is None:
            raise Exception("Event is not found")
        event_request = EventRequest(
            event_id=event.id,
            status=EventRequestStatus.PENDING
        )
        event_request_id = await super().create(event_request)
        return event_request_id is not None

