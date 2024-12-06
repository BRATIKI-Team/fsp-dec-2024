from typing import Annotated, List

from fastapi import Depends

from app.api.dto import SearchReq, Page
from app.api.dto.event_dto import CreateEventReq, ExtendedEvent
from app.data.domains.event import Event
from app.data.repositories.base_repository import T
from app.data.repositories.event_repository import EventRepository
from app.data.repositories.region_repository import RegionRepository
from app.services.base_service import BaseService
from app.services.region_service import RegionService
from app.services.user_service import UserService


class EventService(BaseService[Event]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            region_service: Annotated[RegionService, Depends(RegionService)],
            event_repository: Annotated[EventRepository, Depends(EventRepository)]
    ):
        super().__init__(event_repository)
        self._user_service = user_service
        self._event_repository = event_repository
        self._region_service = region_service

    async def create_event(self, user_id: str, create_event_dto: CreateEventReq) -> bool:
        user = await self._user_service.get(user_id)
        # if user.region_id is None:
        #     raise Exception("Has no permission")
        region_id = "675323b351c0c41c65646946"
        event = Event(
            region_id=region_id,
            member_created_id=region_id,
            name=create_event_dto.name,
            discipline=create_event_dto.discipline,
            description=create_event_dto.description,
            datetime=create_event_dto.datetime,
            is_approved_event=False
        )
        event_id = await super().create(event)
        return event_id is not None

    async def disciplines(self) -> List[str]:
        events = await self.get_all()
        disciplines = set()

        for event in events:
            if event.discipline:
                disciplines.add(event.discipline)

        return list(disciplines)


    async def search(self, req: 'SearchReq') -> Page[Event]:
        page = await self._event_repository.search(req=req)
        #
        # events = page.items
        # extended_events = []
        #
        # for event in events:
        #     region = await self._region_service.get(event.region_id)
        #     user = await self._user_service.get(event.member_created_id)
        #
        #     extended_event = ExtendedEvent(
        #         event=event,
        #         region = region,
        #         user=user
        #     )
        #
        #     extended_events.append(extended_event)
        #
        # page.items = extended_events
        return page
