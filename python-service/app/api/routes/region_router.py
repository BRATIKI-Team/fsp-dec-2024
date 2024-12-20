from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Body

from app.api.dto import SearchReq, Page
from app.api.dto.region_dto import RegionCreateReq
from app.data.domains.region import Region
from app.services.auth_service import AuthService
from app.services.region_service import RegionService

router = APIRouter()


@router.post("/{region_id}/assign-member/{user_id}", name="regions:assign-member")
async def assign_member(
        region_id: str,
        user_id: str,
        require_admin: Annotated[bool, Depends(AuthService.require_admin_or_super_admin)],
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


@router.put("/{region_id}", name="regions:update")
async def update(
        region_id: str,
        region_model: Annotated[Region, Body(...)],
        region_service: Annotated[RegionService, Depends(RegionService)]
) -> bool:
    return await region_service.update(region_id, region_model)


@router.post("/search", name="regions:search")
async def search(
        page: SearchReq,
        region_service: Annotated[RegionService, Depends(RegionService)],
) -> Page[Region]:
    return await region_service.search(page)


@router.post("/create", name="regions:create")
async def create(
        require_super_admin: Annotated[bool, Depends(AuthService.require_super_admin)],
        req: RegionCreateReq,
        region_service: Annotated[RegionService, Depends(RegionService)],
) -> str:
    model = Region(
        name=req.name,
        subject=req.subject,
        is_main=req.is_main,
    )

    return await region_service.create(model)
