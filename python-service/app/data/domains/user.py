from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    password: str

    class Config:
        from_attributes = True