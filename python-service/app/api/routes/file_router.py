from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response

from app.services.file_model_service import FileService

router = APIRouter()

@router.post("/upload", name="files:upload")
async def upload_file(
        file: Annotated[UploadFile, File(...)],
        file_service: Annotated[FileService, Depends(FileService)]
) -> str:
    return await file_service.upload_file(file)


@router.get("/{file_id}/download", name="files:download")
async def download(
        file_id: str,
        file_service: Annotated[FileService, Depends(FileService)]
):
    file = await file_service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    print(file.file_name, file.file_type)

    return Response(
        content=file.file_data,
        media_type=file.file_type,
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{file.file_name}"
        }
    )