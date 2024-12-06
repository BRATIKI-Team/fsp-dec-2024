from typing import Annotated, Optional

from fastapi import Depends
from pydantic import EmailStr

from app.data.domains.region import Region
from app.data.repositories.region_repository import RegionRepository
from app.services.base_service import BaseService

class RegionService(BaseService[Region]):
    def __init__(self, region_repository: Annotated[RegionRepository, Depends(RegionRepository)]):
        super().__init__(region_repository)
        self.region_repository = region_repository

    # async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
    #     return await self.user_repository.get_user_by_email(email)