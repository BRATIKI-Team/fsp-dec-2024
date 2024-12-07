from io import BytesIO
from typing import Annotated

from fastapi import Depends, HTTPException, status
import pandas as pd

from app.data.domains.statistics_file import StatisticsFile
from app.data.repositories.statistics_file_repository import StatisticsFileRepository
from app.data.repositories.statistics_repository import StatisticsRepository
from app.services.base_service import BaseService
from app.services.region_service import RegionService


class StatisticsFileService(BaseService[StatisticsFile]):
    def __init__(
            self,
            region_service: Annotated[RegionService, Depends(RegionService)],
            statistics_file_repository: Annotated[StatisticsFileRepository, Depends(StatisticsFileRepository)],
            statistics_repository: Annotated[StatisticsRepository, Depends(StatisticsRepository)]
    ):
        super().__init__(statistics_file_repository)
        self._region_service = region_service
        self._statistics_file_repository = statistics_file_repository
        self._statistics_repository = statistics_repository

    async def generate_statistics_excel_for_year(self, year: int) -> bool:
        statistics = await self._statistics_repository.filter({"year": year})
        if not statistics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Statistics for year {year} are not found",
            )

        data = []
        for statistic in statistics:
            region = await self._region_service.get(statistic.region_id)
            data.append({
                "Регион": region.subject,
                "Количество региональных команд": statistic.participants_count,
                "Количество региональных мероприятий": statistic.events_count,
                "Количество региональных команд-золото": statistic.first_place_count,
                "Количество региональных команд-серебро": statistic.second_place_count,
                "Количество региональных команд-бронза": statistic.third_place_count,
            })

        df = pd.DataFrame(data)
        print(df)
        # Save the DataFrame to an Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output) as writer:
            df.to_excel(writer, index=False, sheet_name=f"{year}_статистика")
        output.seek(0)

        print(output.getvalue())
        stat_file = await self._statistics_file_repository.find_one({"file_name": f"{year}_статистика.xls"})
        if stat_file:
            await self._statistics_file_repository.delete(stat_file.id)

        stat_file = StatisticsFile(
            file_name=f"{year}_статистика.xls",
            file_type="application/vnd.ms-excel",
            file_data=output.getvalue()
        )

        await self._statistics_file_repository.insert(stat_file)
        return True