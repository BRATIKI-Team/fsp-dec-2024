import json
import random
from datetime import datetime, timedelta
from typing import Annotated, List

from bson import Binary
from fastapi import Depends
from pydantic import BaseModel

from app.data.domains.event import Event
from app.data.domains.file_model import FileModel
from app.data.domains.region import Region
from app.data.domains.team_result import TeamResult, TeamPlace
from app.data.repositories.event_repository import EventRepository
from app.services.base_service import BaseService
from app.services.file_model_service import FileModelService
from app.services.region_service import RegionService
from app.statistics.file_parser_service import FileParserService


class EventInfo(BaseModel):
    name: str
    description: str


class EventSeeder(BaseService[Event]):
    def __init__(
            self,
            event_repository: Annotated[EventRepository, Depends(EventRepository)],
            region_service: Annotated[RegionService, Depends(RegionService)],
            file_model_service: Annotated[FileModelService, Depends(FileModelService)],
            file_parser_service: Annotated[FileParserService, Depends(FileParserService)]
    ):
        super().__init__(event_repository)
        self._region_service = region_service
        self._file_model_service = file_model_service
        self._file_parser_service = file_parser_service

    async def seed(self) -> bool:
        regions = await self._region_service.get_all()
        names = self.__get_names_from_file('app/generator/docs/names.json')
        event_info_list = self.__get_event_info_list_from_file('app/generator/docs/events_info.json')
        for region in regions:
            events = self.__seed_events(region.id, event_info_list)

            for event in events:
                teams_results = self.__seed_teams_results(regions, names)
                event.teams_results = teams_results
                event.result_file_id = await self.generate_results_file(event.name, teams_results)
                await self.create(event)

        return True

    async def generate_results_file(self, event_name: str, team_results: List[TeamResult]) -> str:
        bytes_data = self._file_parser_service.parse_to_results_file(team_results)
        file_model = FileModel(
            file_name=f"{event_name}_results.xls",
            file_data=Binary(bytes_data.getvalue()),
            file_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            uploaded_at=datetime.now()
        )

        return await self._file_model_service.create(file_model)

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

    @staticmethod
    def __get_event_info_list_from_file(file_path: str) -> List[EventInfo]:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        events_info = []
        for item in json_data:
            event_info = EventInfo(
                name=item["name"],
                description=item["description"],
            )
            events_info.append(event_info)

        return events_info

    def __seed_events(self, region_id: str, event_info_list: List[EventInfo]) -> list[Event]:
        events = []
        for year in range(2022, 2025):
            for month in range(1, 13):
                events_month = self.__seed_events_month(year, month, region_id, event_info_list)
                for event in events_month:
                    events.append(event)

        return events

    @staticmethod
    def __seed_events_month(year: int, month: int, region_id: str, event_info_list: List[EventInfo]) -> List[Event]:
        events_month = []
        num_events = random.randint(1, 3)

        for _ in range(num_events):
            day = random.randint(1, 28)
            start_date = datetime(year, month, day)
            duration = random.randint(1, 5)
            end_date = start_date + timedelta(days=duration)
            event_info: EventInfo = random.choice(event_info_list)
            event = Event(
                region_id=region_id,
                name=event_info.name,
                location=f"Location {random.choice(['A', 'B', 'C'])}",
                participants_count=random.randint(50, 200),
                start_date=start_date,
                end_date=end_date,
                discipline=random.choice(
                    ['Информационная Безопасность',
                     'Продуктовое Программирование',
                     'Алгоритмическое Программирование'
                     ]),
                description=event_info.description,
                is_approved_event=random.choice([True, False])
            )

            events_month.append(event)

        return events_month

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
