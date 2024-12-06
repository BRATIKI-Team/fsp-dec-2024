from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Body

from app.data.domains.event_request import EventRequest
from app.services.event_request_service import EventRequestService

router = APIRouter()

#todo: save all endpoints

@router.get("/list-all", name="event-requests:list-all")
async def list_all(
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> List[EventRequest]:
    return await event_request_service.get_all()

@router.get("/by-region/{region_id}", name="event-requests:get-by-region")
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

# todo: only for MEMBER
@router.post("/{event_id}/create_request", name="event-requests:send-request")
async def send_request(
        event_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> bool:
    return await event_request_service.send_event_request(event_id)

# todo: save endpoint for only SUPER_ADMIN
@router.post("/{req_id/set-status", name="event-requests:set-status")
async def set_status(
        req_id: str,
        event_request: Annotated[EventRequest, Body(...)],
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> bool:
    return await event_request_service.set_status(req_id, event_request)

@router.delete("/{req_id}", name="event-requests:delete")
async def set_status(
        req_id: str,
        event_request_service: Annotated[EventRequestService, Depends(EventRequestService)]
) -> bool:
    return await event_request_service.delete(req_id)