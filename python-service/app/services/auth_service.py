from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import MessageSchema, MessageType
from passlib.context import CryptContext

from app.api.dto import RegisterReq, LoginReq, LoginResp, RefreshTokenReq, ForgetPasswordReq, ResetPasswordReq
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, RESET_PASSWORD_TOKEN_URL, \
    RESET_PASSWORD_TOKEN_EXPIRE_MINUTES, APP_NAME, CLIENT_HOST
from app.core.dependencies import get_mail
from app.data.domains.user import User
from app.data.domains.user import UserRole
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

    async def forget_password(self, req: ForgetPasswordReq) -> None:
        user = await self.user_service.get_user_by_email(req.email)

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

        email_body = {
            "company_name": APP_NAME,
            "link_expiry_min": RESET_PASSWORD_TOKEN_EXPIRE_MINUTES,
            "reset_link": forget_url_link,
        }

        email_message = MessageSchema(
            subject="Инструкции по восстановлению пароля.",
            recipients=[user.email],
            template_body=email_body,
            subtype=MessageType.html
        )

        fm = get_mail()

        # TODO use bg tasks
        await fm.send_message(message=email_message)

    async def reset_password(self, req: ResetPasswordReq) -> None:
        email = jwt.decode(req.token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM).get("sub")

        hashed_pwd = self.pwd_context.hash(req.password)
        user = await self.user_service.get_user_by_email(email)

        if user is None or user.id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.password = hashed_pwd

        await self.user_service.update(
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
    def require_member(
            cls,
            token: Annotated[str, Depends(OAuth2PasswordBearer)]
    ) -> None:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_role = payload.get("role")
        if user_role != UserRole.ADMIN or user_role != UserRole.MEMBER:
            raise Exception("You have no permissions")
