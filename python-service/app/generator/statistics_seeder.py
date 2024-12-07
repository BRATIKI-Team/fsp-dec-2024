from typing import Annotated

from fastapi import Depends

from app.data.domains.statistics import Statistics
from app.services.base_service import BaseService
from app.services.event_service import EventService
from app.statistics.statistics_service import StatisticsService


class StatisticsSeeder:
    def __init__(
            self,
            event_service: Annotated[EventService, Depends(EventService)],
            statistics_service: Annotated[StatisticsService, Depends(StatisticsService)]
    ):
        self._event_service = event_service
        self._statistics_service = statistics_service

    async def seed(self) -> bool:
        events = await self._event_service.get_all()
        for event in events:
            await self._statistics_service.on_event_result_added(event)
        return True
