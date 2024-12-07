from typing import Annotated, List

from fastapi import Depends, HTTPException, status

from app.api.dto.event_request_dto import SendEventRequestResult
from app.api.dto.member_request_dto import SendMemberRequestResult
from app.data.domains.member_request import MemberRequest, MemberRequestStatus
from app.data.domains.user import UserRole
from app.data.repositories.member_request_repository import MemberRequestRepository
from app.services.base_service import BaseService
from app.services.user_service import UserService


class MemberRequestService(BaseService[MemberRequest]):
    def __init__(
            self,
            member_request_repository: Annotated[MemberRequestRepository, Depends(MemberRequestRepository)],
            user_service: Annotated[UserService, Depends(UserService)]
    ):
        super().__init__(member_request_repository)
        self._member_request_repository = member_request_repository
        self._user_service = user_service

    async def send_request(self, user_id: str, region_id: str) -> SendMemberRequestResult:
        existing_result = await self._member_request_repository.find_one({"user_id": user_id})
        print(existing_result, "found")
        if existing_result:
            match existing_result.status:
                case MemberRequestStatus.PENDING:
                    return SendMemberRequestResult(erro="request-exists")
                case MemberRequestStatus.APPROVED:
                    return SendMemberRequestResult(error="already-member")

        request = MemberRequest(user_id=user_id, region_id=region_id, status=MemberRequestStatus.PENDING)
        await self._member_request_repository.insert(request)
        return SendEventRequestResult()

    async def get_by_region_id(self, region_id: str) -> List[MemberRequest]:
        return await self._member_request_repository.filter({"region_id": region_id, "status": "pending"})

    async def set_status(self, req_id, req_status: MemberRequestStatus) -> bool:
        req = await self._member_request_repository.get(req_id)
        if not req:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if req_status == MemberRequestStatus.APPROVED:
            user = await self._user_service.get(req.user_id)
            user.region_id = req.region_id
            user.role = UserRole.MEMBER
            await self._user_service.update(user.id, user)

        req.status = req_status
        return await self._member_request_repository.update(req_id, req)
