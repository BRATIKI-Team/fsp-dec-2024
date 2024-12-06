from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.data.domains.region import Region
from app.data.domains.user import UserRole, User
from app.data.repositories.region_repository import RegionRepository
from app.services.base_service import BaseService
from app.services.user_service import UserService


class RegionService(BaseService[Region]):
    def __init__(self, region_repository: Annotated[RegionRepository, Depends(RegionRepository)],
                 user_service: Annotated[UserService, Depends(UserService)]):
        super().__init__(region_repository)
        self.region_repository = region_repository
        self.user_service = user_service

    async def add_user(self, region_id: str, user_id: str) -> bool:
        user = await self.user_service.get(user_id)
        if user is None or user.role != UserRole.USER:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exist"
            )

        region = await  self.region_repository.get(region_id)
        if region is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region does not exist"
            )

        user.role = UserRole.MEMBER
        user.regionId = region_id
        return await self.user_service.update(user_id, user)