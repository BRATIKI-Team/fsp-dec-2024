from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.api.dto import RegisterReq, LoginReq, LoginResp, RefreshTokenReq, ForgetPasswordReq, ResetPasswordReq, \
    RegisterAdminReq
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_PASSWORD_TOKEN_URL, \
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES, CLIENT_HOST
from app.data.domains.user import User
from app.data.domains.user import UserRole
from app.services.mail.mail_service import MailService
from app.services.member_request_service import MemberRequestService
from app.services.user_service import UserService


class AuthService:
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            mail_service: Annotated[MailService, Depends(MailService)],
            member_request_service: Annotated[MemberRequestService, Depends(MemberRequestService)]
    ):
        self._user_service = user_service
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._mail_service = mail_service
        self._member_request_service = member_request_service

    async def register(self, register_dto: RegisterReq, role: UserRole = UserRole.USER) -> str:
        user = await self._user_service.get_user_by_email(register_dto.email)
        if user is not None:
            raise ValueError("User with this email already exists")

        hashed_pwd = self._pwd_context.hash(register_dto.password)
        new_user = User(email=register_dto.email, password=hashed_pwd, role=role)
        user_id = await self._user_service.create(new_user)
        await self._member_request_service.send_request(user_id, register_dto.region_id)
        return user_id

    async def registerForAdmin(self, register_dto: RegisterAdminReq, role: UserRole = UserRole.USER) -> str:
        user = await self.user_service.get_user_by_email(register_dto.email)
        if user is not None:
            raise ValueError("User with this email already exists")

        hashed_pwd = self.pwd_context.hash(register_dto.password)
        new_user = User(email=register_dto.email, password=hashed_pwd, role=role)
        user_id = await self.user_service.create(new_user)
        return user_id

    async def login(self, login_dto: LoginReq) -> LoginResp:
        user = await self._user_service.get_user_by_email(login_dto.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.role == UserRole.USER:
            # As request to become member of region is not accepted, user can't log in to portal
            return LoginResp(id=user.id, email=user.email, error="not-member")
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

        user = await self._user_service.get_user_by_email(user_email)
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

    async def forget_password(self, req: ForgetPasswordReq) -> None:
        user = await self._user_service.get_user_by_email(req.email)

        if user is None or user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        token_payload = {
            "sub": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=RESET_PASSWORD_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(
            payload=token_payload,
            key=JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM
        )

        forget_url_link = f"{CLIENT_HOST}{RESET_PASSWORD_TOKEN_URL}/{token}"

        await self._mail_service.notify_about_password_reset(user.email, forget_url_link)

    async def reset_password(self, req: ResetPasswordReq) -> None:
        email = jwt.decode(req.token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM).get("sub")

        hashed_pwd = self._pwd_context.hash(req.password)
        user = await self._user_service.get_user_by_email(email)

        if user is None or user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.password = hashed_pwd

        await self._user_service.update(
            item_id=user.id,
            item=user
        )

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
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> bool:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.SUPER_ADMIN:
            raise Exception("You have no permissions")
        return True

    @classmethod
    def require_admin(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> bool:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.ADMIN:
            raise Exception("You have no permissions")
        return True

    @classmethod
    def require_admin_or_super_admin(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> bool:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.ADMIN and user_role != UserRole.SUPER_ADMIN:
            raise Exception("You have no permissions")
        return True

    @classmethod
    def require_member(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]
    ) -> bool:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        # ADMIN has the same privileges as MEMBER
        if user_role != UserRole.ADMIN or user_role != UserRole.MEMBER:
            raise Exception("You have no permissions")
        return True
