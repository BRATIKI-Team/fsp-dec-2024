from typing import Annotated

from fastapi import Depends

from app.api.dto.member_request_dto import ExtendedMemberRequest
from app.data.domains.member_request import MemberRequest
from app.services.user_service import UserService


class MemberMapper:
    def __init__(self, user_service: Annotated[UserService, Depends(UserService)]):
        self._user_service = user_service

    async def map_member_to_extend(self, member: MemberRequest) -> ExtendedMemberRequest:
        user = await self._user_service.get(member.user_id)
        userDto = self._user_service.get_user_dto(user, None)

        return ExtendedMemberRequest(
            id=member.id,
            region_id=member.region_id,
            user=userDto,
            status=member.status,
        )
