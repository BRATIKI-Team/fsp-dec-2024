from typing import Annotated

from fastapi import Depends

from app.services.event_service import EventService
from app.statistics.statistics_file_service import StatisticsFileService
from app.statistics.statistics_service import StatisticsService


class StatisticsSeeder:
    def __init__(
            self,
            event_service: Annotated[EventService, Depends(EventService)],
            statistics_service: Annotated[StatisticsService, Depends(StatisticsService)],
            statistics_file_service: Annotated[StatisticsFileService, Depends(StatisticsFileService)]
    ):
        self._event_service = event_service
        self._statistics_service = statistics_service
        self._statistics_file_service = statistics_file_service

    async def seed(self) -> bool:
        events = await self._event_service.get_all()
        for event in events:
            await self._statistics_service.on_event_result_added(event)

        await self._statistics_file_service.generate_statistics_excel_for_year(2022)
        await self._statistics_file_service.generate_statistics_excel_for_year(2023)
        await self._statistics_file_service.generate_statistics_excel_for_year(2024)

        return True
