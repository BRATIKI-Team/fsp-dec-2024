from io import BytesIO
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.dependencies import transliterate
from app.data.domains.statistics_file import StatisticsFile
from app.statistics.statistics_file_service import StatisticsFileService

router = APIRouter()

@router.get("/list-all", name="statistics:list-all")
async def list_all_statistics(
        statistics_file_service: Annotated[StatisticsFileService, Depends(StatisticsFileService)]
) -> List[StatisticsFile]:
    return await statistics_file_service.get_all()

@router.get("/{file_id}/download", name="statistics:download")
async def download(
        file_id: str,
        statistics_file_service: Annotated[StatisticsFileService, Depends(StatisticsFileService)]
):
    file = await statistics_file_service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    print(file.file_name, file.file_type)
    file = await statistics_file_service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_data = BytesIO(file.file_data)
    return StreamingResponse(
        file_data,
        media_type=file.file_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{transliterate(file.file_name)}"
        }
    )