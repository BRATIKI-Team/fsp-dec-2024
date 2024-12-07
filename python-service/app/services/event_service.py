import json
import random
from datetime import datetime, timedelta
from typing import Annotated, List

from fastapi import Depends

from app.api.dto import SearchReq, Page
from app.api.dto.event_dto import CreateEventReq
from app.data.domains.event import Event
from app.data.domains.region import Region
from app.data.domains.team_result import TeamResult, TeamPlace
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

    async def seed(self) -> bool:
        regions = await self._region_service.get_all()
        names = self.__get_names_from_file('app/generator/docs/names.json')
        for region in regions:
            events = self.__seed_events(region.id)

            for event in events:
                teams_results = self.__seed_teams_results(regions, names)
                event.teams_results = teams_results
                await self.create(event)

        return True

    @staticmethod
    def __get_names_from_file(file_path: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                team_names = json.load(file)
                if isinstance(team_names, list):
                    return team_names
                else:
                    raise ValueError("JSON data is not a list.")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []

    def __seed_events(self, region_id: str) -> list[Event]:
        events = []
        for year in range(2022, 2025):
            for month in range(1, 13):
                event = self.__seed_event(year, month, region_id)
                events.append(event)

        return events

    @staticmethod
    def __seed_event(year: int, month: int, region_id: str) -> Event:

        num_events = random.randint(1, 10)

        for _ in range(num_events):
            day = random.randint(1, 28)
            start_date = datetime(year, month, day)
            duration = random.randint(1, 5)
            end_date = start_date + timedelta(days=duration)

            event = Event(
                region_id=region_id,
                name=f"Event {random.randint(1, 1000)}",  # Randomly generate event names
                location=f"Location {random.choice(['A', 'B', 'C'])}",  # Random location
                participants_count=random.randint(50, 200),  # Random number of participants
                start_date=start_date,
                end_date=end_date,
                discipline=random.choice(
                    ['Информационная Безопасность', 'Продуктовое Программирование', 'Алгоритмическое Программирование']),
                description="Auto-generated event",
                is_approved_event=random.choice([True, False])
            )

            return event

    @staticmethod
    def __seed_teams_results(regions: List[Region], names: List[str]) -> List[TeamResult]:

        team_results = []
        count_teams = random.randint(3, 30)
        names = random.sample(names, count_teams)

        for i in range(count_teams):
            random_region_id = random.choice(regions).id
            team_name = names[i]

            team_result = TeamResult(
                name=team_name,
                region_id=random_region_id
            )

            team_results.append(team_result)

        top_teams = random.sample(team_results, 3)
        top_teams[0].place = TeamPlace.FIRST
        top_teams[1].place = TeamPlace.SECOND
        top_teams[2].place = TeamPlace.THIRD

        return team_results
