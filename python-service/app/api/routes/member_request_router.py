from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.api.dto.member_request_dto import SendMemberRequestResult
from app.data.domains.member_request import MemberRequest, MemberRequestStatus
from app.services.auth_service import AuthService
from app.services.member_request_service import MemberRequestService

router = APIRouter()

@router.get("/{region_id}", name="member-requests:list-by-region-id")
async def list_by_region_id(
        region_id: str,
        member_request_service: Annotated[MemberRequestService, Depends(MemberRequestService)]
) -> List[MemberRequest]:
    return await member_request_service.get_by_region_id(region_id)

@router.post("/{region_id}/send-request", name="member-requests:send-request")
async def send_request(
        region_id: str,
        user_id: Annotated[str, Depends(AuthService.require_user_id)],
        member_request_service: Annotated[MemberRequestService, Depends(MemberRequestService)]
) -> SendMemberRequestResult:
    return await member_request_service.send_request(user_id, region_id)

@router.post("/{region_id}/send-request/test/{user_id}", name="member-requests:send-request")
async def send_request(
        region_id: str,
        user_id: str,
        member_request_service: Annotated[MemberRequestService, Depends(MemberRequestService)]
) -> SendMemberRequestResult:
    return await member_request_service.send_request(user_id, region_id)

@router.post("/{req_id}/set-status/{status}", name="member-requests:set-status")
async def set_status(
        req_id: str,
        status: MemberRequestStatus,
        # require_admin: Annotated[bool, Depends(AuthService.require_admin)],
        member_request_service: Annotated[MemberRequestService, Depends(MemberRequestService)]
) -> bool:
    return await member_request_service.set_status(req_id, status)
