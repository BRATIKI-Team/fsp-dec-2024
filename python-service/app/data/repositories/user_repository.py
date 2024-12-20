from typing import Annotated, Dict, Optional

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr

from app.core.dependencies import get_db
from app.data.domains.user import User, UserRole
from app.data.repositories.base_repository import BaseRepository, T


class UserRepository(BaseRepository):
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        super().__init__(db, "users")

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        document = await self.collection.find_one({"email": email})
        return self._document_to_model(document) if document else None

    def serialize(self, document: Dict) -> User:
        return User(**document)
