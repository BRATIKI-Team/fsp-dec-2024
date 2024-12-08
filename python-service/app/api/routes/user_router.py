from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Body

from app.api.dto import RegisterReq, LoginReq, LoginResp, RefreshTokenReq, ForgetPasswordReq, ResetPasswordReq, \
    RegisterDto
from app.api.dto.user_dto import UserDto
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", name="users:register")
async def register(
        register_dto: Annotated[RegisterReq, Body(...)],
        auth_service: Annotated[AuthService, Depends(AuthService)]
) -> RegisterDto:
    user_id = await auth_service.register(register_dto)
    return RegisterDto(id=user_id)


@router.post("/login", name="users:login")
async def login(
        login_dto: Annotated[LoginReq, Body(...)],
        auth_service: Annotated[AuthService, Depends(AuthService)]
) -> LoginResp:
    return await auth_service.login(login_dto)


@router.put('/forget', name="users:forget")
async def reset(
        forget_dto: Annotated[ForgetPasswordReq, Body(...)],
        auth_service: Annotated[AuthService, Depends(AuthService)]
) -> None:
    return await auth_service.forget_password(forget_dto)


@router.put('/reset', name="users:reset")
async def reset(
        reset_dto: Annotated[ResetPasswordReq, Body(...)],
        auth_service: Annotated[AuthService, Depends(AuthService)]
) -> None:
    return await auth_service.reset_password(reset_dto)


@router.post("/refresh-token", name="users:refresh-token")
async def refresh_token(
        refresh_token_req: Annotated[RefreshTokenReq, Body(...)],
        auth_service: Annotated[AuthService, Depends(AuthService)]
) -> LoginResp:
    return await auth_service.refresh_token(refresh_token_req)


@router.get("/get-all", name="users:get-all")
async def get_all(
        user_service: Annotated[UserService, Depends(UserService)]
) -> List[UserDto]:
    return await user_service.get_all()


@router.get("/me", name="users:me")
async def get_me(
        user_id: Annotated[str, Depends(AuthService.require_user_id)],
        user_service: Annotated[UserService, Depends(UserService)]
) -> UserDto:
    return await user_service.get_me(user_id)


@router.get("/{user_id}", name="users:get-by-id")
async def get_by_id(
        user_id: str,
        user_service: Annotated[UserService, Depends(UserService)]
) -> Optional[UserDto]:
    return await user_service.get_me(user_id)


@router.delete("/{user_id}", name="users:delete-by-id")
async def delete_by_id(
        user_id: str,
        user_service: Annotated[UserService, Depends(UserService)]
) -> bool:
    return await user_service.delete(user_id)
