from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import Depends

from app.api.dto import SearchReq, Page
from app.api.dto.event_dto import CreateEventReq, ExtendedEvent
from app.data.domains.event import Event
from app.data.domains.file_model import FileModel
from app.data.repositories.event_repository import EventRepository
from app.services.base_service import BaseService
from app.services.file_model_service import FileModelService
from app.services.region_service import RegionService
from app.services.user_service import UserService


class EventService(BaseService[Event]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            region_service: Annotated[RegionService, Depends(RegionService)],
            event_repository: Annotated[EventRepository, Depends(EventRepository)],
            file_service: Annotated[FileModelService, Depends(FileModelService)]
    ):
        super().__init__(event_repository)
        self._user_service = user_service
        self._event_repository = event_repository
        self._region_service = region_service
        self._file_service = file_service

    async def create_event(self, user_id: str, create_event_dto: CreateEventReq) -> Event:
        user = await self._user_service.get(user_id)
        if user.region_id is None:
             raise Exception("Has no permission")

        event = Event(
            region_id=user.region_id,
            member_created_id=user_id,
            name=create_event_dto.name,
            discipline=create_event_dto.discipline,
            description=create_event_dto.description,
            datetime=create_event_dto.datetime,
            documents_ids=create_event_dto.documents_ids,
            protocols_ids=create_event_dto.protocols_ids,
            is_approved_event=False
        )

        event_id = await super().create(event)
        event.id = event_id
        return event

    async def disciplines(self) -> List[str]:
        events = await self.get_all()
        disciplines = set()

        for event in events:
            if event.discipline:
                disciplines.add(event.discipline)

        return list(disciplines)

    async def search(self, req: 'SearchReq') -> Page[ExtendedEvent]:
        page = await self._event_repository.search(req=req)
        extended_events = []
        for event in page.items:
            user = await self._user_service.get(event.member_created_id)
            region = await self._region_service.get(event.region_id)

            documents = [doc.get_dto() for doc in await self._file_service.get_many(event.documents_ids)]
            protocols = [doc.get_dto() for doc in await self._file_service.get_many(event.protocols_ids)]

            extended_events.append(ExtendedEvent(event=event, user=user, region=region, documents=documents, protocols=protocols))

        return Page(
            total=page.total,
            page=page.page,
            page_size=page.page_size,
            items=extended_events,
            more=page.more
        )

    async def seed(self, region_id: str) -> bool:
        events = self.__stub_events(region_id)
        for event in events:
            await self.create(event)

        return True

    @staticmethod
    def __stub_events(region_id: str) -> list[Event]:
        start_date = datetime.now()
        end_date = start_date + timedelta(days=5)

        return [
            Event(
                region_id=region_id,
                name="Event One",
                location="Город проведения 1",
                participants_count=100,
                start_date=start_date,
                end_date=end_date,
                discipline="Discipline A",
                description="Description for Event One",
                documents_ids=[],
                protocols_ids=[],
                is_approved_event=False
            ),
            Event(
                region_id=region_id,
                name="Event Two",
                location="Город проведения 2",
                participants_count=100,
                start_date=start_date,
                end_date=end_date,
                discipline="Discipline B",
                description="Description for Event Two",
                documents_ids=[],
                protocols_ids=[],
                is_approved_event=True
            ),
            Event(
                region_id=region_id,
                name="Event Three",
                location="Город проведения 3",
                participants_count=100,
                start_date=start_date,
                end_date=end_date,
                discipline="Discipline C",
                description="Description for Event Three",
                documents_ids=[],
                protocols_ids=[],
                is_approved_event=False
            )
        ]
