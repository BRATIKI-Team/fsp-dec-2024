from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from pydantic import EmailStr
from starlette import status

from app.api.dto.region_dto import RegionDto
from app.api.dto.user_dto import UserDto
from app.data.repositories.region_repository import RegionRepository
from app.data.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.data.domains.user import User, UserRole


class UserService(BaseService[User]):
    def __init__(
            self,
            user_repository: Annotated[UserRepository, Depends(UserRepository)],
            region_repository: Annotated[RegionRepository, Depends(RegionRepository)]):
        super().__init__(user_repository)
        self._user_repository = user_repository
        self._region_repository = region_repository

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        return await self._user_repository.get_user_by_email(email)

    async def seed_super_admin(self) -> bool:
        await self.create(
            User(
                email="superadmin@gmail.com",
                password="123123",
                role=UserRole.SUPER_ADMIN
            )
        )
        return True

    async def get_me(self, user_id: str) -> UserDto:
        user = await self._user_repository.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")


        region_model = None if user.region_id is None else await self._region_repository.get(user.region_id)
        region_admin = None
        if region_model is not None and region_model.admin_id is not None:
            region_admin = await self._user_repository.get(region_model.admin_id)

        admin_dto = None
        if region_admin is not None:
            admin_dto = None if region_admin is None else UserDto(
                id=region_admin.id,
                email=region_admin.email,
                role=region_admin.role,
                region=None
            )

        region_dto = None if not region_model else RegionDto(
            id=region_model.id,
            name=region_model.name,
            description=region_model.description,
            is_main=region_model.is_main,
            contacts=region_model.contacts,
            admin=admin_dto
        )

        user_dto = UserDto(
            id=user.id,
            email=user.email,
            role=user.role,
            region=region_dto
        )
        return user_dto