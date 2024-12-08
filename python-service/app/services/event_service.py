from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, UploadFile, HTTPException, status

from app.api.dto import SearchReq, Page
from app.api.dto.event_dto import CreateEventReq
from app.data.domains.event import Event
from app.data.repositories.event_repository import EventRepository
from app.generator.event_seeder import EventSeeder
from app.services.base_service import BaseService
from app.services.file_model_service import FileModelService
from app.services.region_service import RegionService
from app.services.user_service import UserService
from app.statistics.file_parser_service import FileParserService
from app.statistics.statistics_service import StatisticsService


class EventService(BaseService[Event]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            region_service: Annotated[RegionService, Depends(RegionService)],
            event_repository: Annotated[EventRepository, Depends(EventRepository)],
            event_seeder: Annotated[EventSeeder, Depends(EventSeeder)],
            file_service: Annotated[FileModelService, Depends(FileModelService)],
            file_parser_service: Annotated[FileParserService, Depends(FileParserService)],
            statistics_service: Annotated[StatisticsService, Depends(StatisticsService)]
    ):
        super().__init__(event_repository)
        self._user_service = user_service
        self._event_repository = event_repository
        self._region_service = region_service
        self._file_service = file_service
        self._event_seeder = event_seeder
        self._file_parser_service = file_parser_service
        self._statistics_service = statistics_service

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
            start_date=create_event_dto.start_date,
            end_date=create_event_dto.end_date,
            participants_count=create_event_dto.participants_count,
            location=create_event_dto.location,
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

    async def search(self, req: SearchReq) -> Page[Event]:
        return await self._event_repository.search(req=req)

    async def region_events_for_year(self, region_id: str, year: int) -> List[Event]:
        start_of_year = datetime(year, 1, 1)
        filters = {
            "region_id": region_id,
            "start_date": {"$gte": start_of_year}
        }

        return await self._event_repository.filter(filters)

    async def upload_result(self, event_id: str, file: UploadFile) -> str:
        event = await self._event_repository.get(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        file_id = await self._file_service.upload_file(file)
        await file.seek(0)
        team_results = await self._file_parser_service.parse_from_results_file(file)
        event.result_file_id = file_id
        event.teams_results = team_results

        await self._event_repository.update(event_id, event)
        await self._statistics_service.on_event_result_added(event)

        return file_id

    async def seed(self) -> bool:
        return await self._event_seeder.seed()
