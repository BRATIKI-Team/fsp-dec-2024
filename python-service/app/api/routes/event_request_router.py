from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Body

from app.api.dto.event_request_dto import SendEventRequestResult, EventRequestDto
from app.data.domains.event_request import EventRequest
from app.data.mappers.event_request_mapper import EventRequestMapper
from app.services.auth_service import AuthService
from app.services.event_request_service import EventRequestService

router = APIRouter()


# todo: save all endpoints

@router.get("/list-all", name="event-requests:list-all")
async def list_all(
        require_super_admin: Annotated[bool, Depends(AuthService.require_super_admin)],
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)],
        req_mapper: Annotated[EventRequestMapper, Depends(EventRequestMapper)],
) -> List[EventRequestDto]:
    reqs = await event_request_service.get_pending()
    extended_reqs = []
    for req in reqs:
        extended_reqs.append(await req_mapper.map_req_to_extend(req))
    return extended_reqs


@router.get("/{region_id}/by-region", name="event-requests:get-by-region")
async def get_by_region_id(
        region_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> List[EventRequest]:
    return await event_request_service.get_by_region_id(region_id)


@router.get("/{req_id}", name="event-requests:get-by-id")
async def get_by_id(
        req_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> Optional[EventRequest]:
    return await event_request_service.get(req_id)


@router.get("/{event_id}/by-event-id", name="event-requests:get-by-event-id")
async def get_by_event_id(
        event_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> Optional[EventRequest]:
    return await event_request_service.get_by_event_id(event_id)


# todo: only for MEMBER
@router.post("/{event_id}/send_request", name="event-requests:send-request")
async def send_request(
        event_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> SendEventRequestResult:
    return await event_request_service.send_event_request(event_id)


# todo: save endpoint for only SUPER_ADMIN
@router.post("/{req_id}/set-status", name="event-requests:set-status")
async def set_status(
        req_id: str,
        event_request: Annotated[EventRequest, Body(...)],
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> bool:
    return await event_request_service.set_status(req_id, event_request)


@router.delete("/{req_id}", name="event-requests:delete")
async def delete(
        req_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> bool:
    return await event_request_service.delete(req_id)
