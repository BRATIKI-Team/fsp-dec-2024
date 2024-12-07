from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.dto import SearchReq, Page
from app.core.dependencies import get_db
from app.data.domains.region import Region
from app.data.repositories.base_repository import BaseRepository, T
from app.data.repositories.region_filter_repository import RegionFilterRepository


class RegionRepository(BaseRepository):
    def __init__(self,
                 db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
                 filter_repository: Annotated[RegionFilterRepository, Depends(RegionFilterRepository)],
                 ):
        super().__init__(db, "regions")
        self._filter_repository = filter_repository

    # async def get_user_by_email(self, email: EmailStr) -> Optional[Region]:
    #     document = await self.collection.find_one({"email": email})
    #     return self._document_to_model(document) if document else None

    def serialize(self, document: Dict) -> T:
        return Region(**document)

    async def search(self, req: SearchReq) -> Page[Region]:
        return await self.paginate(
            cursor=self._filter_repository.apply(self.collection, req=req),
            req=req
        )
