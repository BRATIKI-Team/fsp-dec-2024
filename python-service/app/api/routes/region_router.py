from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.data.domains.region import Region
from app.services.auth_service import AuthService
from app.services.region_service import RegionService
from app.services.user_service import UserService

router = APIRouter()

@router.post("/add-user", name="regions:add-user")
async def add_user(
        check: Annotated[None, Depends(AuthService.require_super_admin)],
        region_service: Annotated[RegionService, Depends(RegionService)],
        user_service: Annotated[UserService, Depends(UserService)],
        region_id: str,
        user_id: str
) -> bool:
    return await region_service.add_user(region_id, user_id)

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