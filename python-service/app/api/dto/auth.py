from pydantic import BaseModel, EmailStr

class RegisterDto(BaseModel):
    id: str

class RegisterReq(BaseModel):
    email: EmailStr
    password: str


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class LoginResp(BaseModel):
    id: str
    email: EmailStr
    token: str
    refresh_token: str


class ForgetPasswordReq(BaseModel):
    email: EmailStr


class ResetPasswordReq(BaseModel):
    token: str
    password: str


class RefreshTokenReq(BaseModel):
    refresh_token: str
