from typing import List, Annotated

from fastapi import APIRouter, Depends

from app.data.domains.statistics_file import StatisticsFile
from app.statistics.statistics_file_service import StatisticsFileService

router = APIRouter()

@router.get("/list-all", name="statistics:list-all")
async def list_all_statistics(
        statistics_file_service: Annotated[StatisticsFileService, Depends(StatisticsFileService)]
) -> List[StatisticsFile]:
    return await statistics_file_service.get_all()