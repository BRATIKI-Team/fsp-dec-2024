from typing import Annotated

from fastapi import Depends

from app.data.domains.event import Event
from app.data.domains.statistics import Statistics
from app.data.domains.team_result import TeamPlace
from app.data.repositories.statistics_repository import StatisticsRepository
from app.services.region_service import RegionService


class StatisticsService:
    def __init__(
            self,
            region_service: Annotated[RegionService, Depends(RegionService)],
            statistics_repository: Annotated[StatisticsRepository, Depends(StatisticsRepository)]
    ):
        self._region_service = region_service
        self._statistics_repository = statistics_repository


    async def on_event_result_added(self, event: Event) -> None:
        region_stat = await self._statistics_repository.find_one({"region_id": event.region_id, "year": event.start_date.year})
        region_stat_id = None if not region_stat else region_stat.id
        if not region_stat:
            region_stat = Statistics.get_default(event.region_id, event.start_date.year)
            region_stat_id = await self._statistics_repository.insert(region_stat)
        region_stat.events_count += 1
        await self._statistics_repository.update(region_stat_id, region_stat)

        for team_result in event.teams_results:
            team_region_stat = await self._statistics_repository.find_one({"region_id": team_result.region_id, "year": event.start_date.year})
            team_region_stat_id = None if not team_region_stat else team_region_stat.id
            if not team_region_stat:
                team_region_stat = Statistics.get_default(team_result.region_id, year=event.start_date.year)
                team_region_stat_id = await self._statistics_repository.insert(team_region_stat)

            team_region_stat.participants_count += 1
            match team_result.place:
                case TeamPlace.FIRST:
                    team_region_stat.first_place_count += 1
                case TeamPlace.SECOND:
                    team_region_stat.second_place_count += 1
                case TeamPlace.THIRD:
                    team_region_stat.third_place_count += 1

            await self._statistics_repository.update(team_region_stat_id, team_region_stat)

