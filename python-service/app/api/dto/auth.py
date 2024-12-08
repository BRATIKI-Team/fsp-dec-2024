from typing import Optional

from pydantic import BaseModel, EmailStr

class RegisterDto(BaseModel):
    id: str

class RegisterReq(BaseModel):
    email: EmailStr
    region_id: str
    password: str


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class LoginResp(BaseModel):
    id: str
    email: EmailStr
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    error: Optional[str] = None


class ForgetPasswordReq(BaseModel):
    email: EmailStr


class ResetPasswordReq(BaseModel):
    token: str
    password: str


class RefreshTokenReq(BaseModel):
    refresh_token: str
