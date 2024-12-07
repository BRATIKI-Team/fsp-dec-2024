from io import BytesIO
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.core.dependencies import transliterate
from app.data.domains.file_model import FileModel
from app.services.file_model_service import FileModelService

router = APIRouter()


@router.get("/list-all", name="files:list-all")
async def list_all(
        file_service: Annotated[FileModelService, Depends(FileModelService)]
) -> List[FileModel]:
    return await file_service.get_all()


@router.post("/upload", name="files:upload")
async def upload_file(
        file: Annotated[UploadFile, File(...)],
        file_service: Annotated[FileModelService, Depends(FileModelService)]
) -> str:
    return await file_service.upload_file(file)


@router.get("/{file_id}/download", name="files:download")
async def download(
        file_id: str,
        file_service: Annotated[FileModelService, Depends(FileModelService)]
):
    file = await file_service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    print(file.file_name, file.file_type)
    file = await file_service.get(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_data = BytesIO(file.file_data)
    return StreamingResponse(
        file_data,
        media_type=file.file_type,
        headers={
            "Content-Disposition": f"inline; filename*=UTF-8''{transliterate(file.file_name)}",
            "Content-Type": "application/octet-stream"
        }
    )


@router.delete("/{file_id", name="files:delete-by-id")
async def delete(
        file_id: str,
        file_service: Annotated[FileModelService, Depends(FileModelService)]
) -> bool:
    return await file_service.delete(file_id)
