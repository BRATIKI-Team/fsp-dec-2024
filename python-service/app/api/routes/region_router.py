from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.data.domains.region import Region
from app.services.auth_service import AuthService
from app.services.region_service import RegionService

router = APIRouter()


@router.post("/{region_id}/assign-member/{user_id}", name="regions:assign-member")
async def assign_member(
        region_id: str,
        user_id: str,
        require_admin: Annotated[bool, Depends(AuthService.require_admin)],
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> bool:
    return await region_service.assign_member(region_id, user_id)


@router.post("/{region_id}/assign-admin/{user_id}", name="regions:assign-admin")
async def assign_admin(
        region_id: str,
        user_id: str,
        require_super_admin: Annotated[bool, Depends(AuthService.require_super_admin)],
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> bool:
    return await region_service.assign_admin(region_id, user_id)


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
