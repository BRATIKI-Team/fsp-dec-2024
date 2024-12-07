from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dto import SearchReq, Page
from app.data.domains.region import Region
from app.data.domains.user import UserRole
from app.data.repositories.region_repository import RegionRepository
from app.generator.region_seeder import RegionSeeder
from app.services.base_service import BaseService
from app.services.user_service import UserService


class RegionService(BaseService[Region]):
    def __init__(
            self,
            region_repository: Annotated[RegionRepository, Depends(RegionRepository)],
            region_seeder: Annotated[RegionSeeder, Depends(RegionSeeder)],
            user_service: Annotated[UserService, Depends(UserService)]):
        super().__init__(region_repository)
        self._region_repository = region_repository
        self._region_seeder = region_seeder
        self._user_service = user_service

    async def seed(self) -> bool:
        return await self._region_seeder.seed()

    async def assign_admin(self, region_id: str, user_id: str) -> bool:
        return await self.__assign_user_internal(region_id, user_id, UserRole.ADMIN)

    async def assign_member(self, region_id: str, user_id: str) -> bool:
        return await self.__assign_user_internal(region_id, user_id, UserRole.MEMBER)

    async def get_by_subject(self, subject: str) -> Region:
        return await self._region_repository.find_one({"subject": subject})

    async def __assign_user_internal(self, region_id: str, user_id: str, role: UserRole) -> bool:
        user = await self._user_service.get(user_id)
        if user is None or user.role != UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist or role is not default"
            )

        region = await  self._region_repository.get(region_id)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region does not exist"
            )

        user.role = role
        user.region_id = region_id

        if role == UserRole.ADMIN:
            region.admin_id = user.id
            await self._region_repository.update(region.id, region)
        return await self._user_service.update(user_id, user)

    async def search(self, req: SearchReq) -> Page[Region]:
        return await self._region_repository.search(req=req)
