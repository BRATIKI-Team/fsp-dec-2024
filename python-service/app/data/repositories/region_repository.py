from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.region import Region
from app.data.repositories.base_repository import BaseRepository, T


class RegionRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "regions")

    # async def get_user_by_email(self, email: EmailStr) -> Optional[Region]:
    #     document = await self.collection.find_one({"email": email})
    #     return self._document_to_model(document) if document else None

    def serialize(self, document: Dict) -> T:
        return Region(**document)
