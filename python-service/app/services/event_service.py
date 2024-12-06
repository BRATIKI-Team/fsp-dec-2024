from typing import Annotated

from fastapi import Depends

from app.api.dto import SearchReq, Page
from app.api.dto.event_dto import CreateEventReq
from app.data.domains.event import Event
from app.data.repositories.base_repository import T
from app.data.repositories.event_repository import EventRepository
from app.services.base_service import BaseService
from app.services.user_service import UserService


class EventService(BaseService[Event]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            event_repository: Annotated[EventRepository, Depends(EventRepository)]
    ):
        super().__init__(event_repository)
        self._user_service = user_service
        self._event_repository = event_repository

    async def create_event(self, user_id: str, create_event_dto: CreateEventReq) -> bool:
        user = await self._user_service.get(user_id)
        # if user.region_id is None:
        #     raise Exception("Has no permission")
        region_id = "6752f8b0f03f50dc0e8f5244"
        event = Event(
            region_id=region_id,
            member_created_id=region_id,
            name=create_event_dto.name,
            discipline=create_event_dto.discipline,
            description=create_event_dto.description,
            datetime=create_event_dto.datetime
        )
        event_id = await super().create(event)
        return event_id is not None

    async def search(self, req: SearchReq) -> Page[T]:
        return await self._event_repository.search(req=req)
