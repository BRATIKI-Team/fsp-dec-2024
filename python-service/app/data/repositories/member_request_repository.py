from typing import Annotated, Dict

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_db
from app.data.domains.member_request import MemberRequest
from app.data.repositories.base_repository import BaseRepository, T


class MemberRequestRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "member-requests")

    def serialize(self, document: Dict) -> T:
        return MemberRequest(**document)