from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Depends, Body

from app.api.dto.event_dto import CreateEventReq
from app.data.domains.event import Event
from app.services.auth_service import AuthService
from app.services.event_service import EventService

router = APIRouter()

@router.get("/list-all", name="events:list-all")
async def list_all(
        event_service: Annotated[EventService, Depends(EventService)]
) -> List[Event]:
    return await event_service.get_all()

@router.get("/{event_id}", name="events:get-by-id")
async def get_by_id(
        event_id: str,
        event_service: Annotated[EventService, Depends(EventService)]
) -> Event:
    return await event_service.get(event_id)

@router.post("/", name="events:create")
async def create_event(
        user_id: Annotated[str, Depends(AuthService.require_user_id)],
        create_event_dto: Annotated[CreateEventReq, Body(...)],
        event_service: Annotated[EventService, Depends(EventService)]
) -> bool:
    pass

@router.post("/{event_id}/create_request", name="events:create-request")
async def create_request(
        event_id: str,
        event_service: Annotated[EventService, Depends(EventService)]
) -> bool:
    return await event_service.create_request_for_event(event_id)

@router.get("/filter", name="events:filter")
async def filter_events(
        event_service: Annotated[EventService, Depends(EventService)]
) -> List[Event]:
    pass