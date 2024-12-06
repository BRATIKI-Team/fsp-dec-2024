from typing import Annotated, Optional

from fastapi import Depends
from pydantic import EmailStr, UUID1

from app.data.repositories.user_repository import UserRepository
from app.services.base_service import BaseService
from app.data.domains.user import User, UserRole


class UserService(BaseService[User]):
    def __init__(self, user_repository: Annotated[UserRepository, Depends(UserRepository)]):
        super().__init__(user_repository)
        self.user_repository = user_repository

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        return await self.user_repository.get_user_by_email(email)

    async def seeder_super_admin(self) -> bool:
        await self.create(
            User(
                email="superadmin@gmail.com",
                password="123123",
                role=UserRole.SUPER_ADMIN
            )
        )
        return True