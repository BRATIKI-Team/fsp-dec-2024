from typing import Optional
from enum import Enum

from pydantic import BaseModel

class UserRole(Enum):
    SUPER_ADMIN = "super-admin",
    ADMIN = "admin",
    REPRESENTOR = "representor"
    USER = "user"

class User(BaseModel):
    id: Optional[str] = None
    email: str
    password: str
    role: UserRole

    class Config:
        from_attributes = True

