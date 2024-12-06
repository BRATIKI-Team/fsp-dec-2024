from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    SUPER_ADMIN = "super-admin",
    ADMIN = "admin",
    MEMBER = "member"
    USER = "user"


class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str
    role: UserRole
    region_id: Optional[str] = None

    class Config:
        from_attributes = True
