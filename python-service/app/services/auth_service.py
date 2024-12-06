from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated

import jwt
from dns.dnssecalgs import algorithms
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.api.dto import RegisterReq, LoginReq, LoginResp, RefreshTokenReq, ForgetPasswordReq
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.data.domains.user import User, UserRole
from app.services.user_service import UserService


class AuthService:
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)]
    ):
        self.user_service = user_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register(self, register_dto: RegisterReq, role: UserRole = UserRole.USER) -> bool:
        user = await self.user_service.get_user_by_email(register_dto.email)
        if user is not None:
            raise ValueError("User with this email already exists")

        hashed_pwd = self.pwd_context.hash(register_dto.password)
        new_user = User(email=register_dto.email, password=hashed_pwd, role=role)
        user_id = await self.user_service.create(new_user)
        return user_id is not None

    async def login(self, login_dto: LoginReq) -> LoginResp:
        user = await self.user_service.get_user_by_email(login_dto.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self.complete_user_login(user)

    async def refresh_token(self, refresh_token_req: Annotated[RefreshTokenReq, Depends(RefreshTokenReq)]):
        payload = jwt.decode(refresh_token_req.refresh_token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_service.get_user_by_email(user_email)
        if not User:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return self.complete_user_login(user)

    def complete_user_login(self, user: User) -> LoginResp:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=7)

        creds = {"id": user.id, "sub": user.email, "role": user.role}
        access_token = self.create_access_token(creds, access_token_expires)
        refresh_token = self.create_access_token(creds, refresh_token_expires)
        return LoginResp(
            id=user.id,
            email=user.email,
            token=access_token,
            refresh_token=refresh_token
        )

    # async def forget_password(self, request: ForgetPasswordReq):

    @classmethod
    def create_access_token(cls, data: dict, expire_date: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expire_date
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @classmethod
    def require_user_id(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> str:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    @classmethod
    def require_super_admin(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer)]
    ) -> None:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.SUPER_ADMIN:
            raise Exception("You have no permissions")

    @classmethod
    def require_representor(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer)]
    ) -> None:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.ADMIN or user_role != UserRole.REPRESENTOR:
            raise Exception("You have no permissions")
