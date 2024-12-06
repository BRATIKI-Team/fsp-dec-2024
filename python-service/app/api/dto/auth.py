from pydantic import BaseModel

class RegisterReq(BaseModel):
    email: str
    password: str

class LoginReq(BaseModel):
    email: str
    password: str

class LoginResp(BaseModel):
    id: str
    email: str
    token: str
    refresh_token: str

class ForgetPasswordReq(BaseModel):
    email: str

class RefreshTokenReq(BaseModel):
    refresh_token: str