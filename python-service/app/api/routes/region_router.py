from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.data.domains.region import Region
from app.services.region_service import RegionService

router = APIRouter()

@router.get("/get-all", name="regions:get-all")
async def get_all(
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> List[Region]:
    return await region_service.get_all()

@router.get("/{region_id}", name="regions:get-by-id")
async def get_by_id(
        region_id: str,
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> Optional[Region]:
    return await region_service.get(region_id)