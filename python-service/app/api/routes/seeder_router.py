from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.region_service import RegionService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/regions", name="seeders:regions")
async def regions(
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> bool:
    return await region_service.seeder()


@router.post("/super-admin", name="seeders:super-admin")
async def super_admin(
        user_service: Annotated[UserService, Depends(UserService)]
) -> bool:
    return await user_service.seeder_super_admin()
