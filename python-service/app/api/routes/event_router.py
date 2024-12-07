from typing import Annotated, List, Optional

from fastapi import APIRouter
from fastapi.params import Depends, Body

from app.api.dto import Page, SearchReq
from app.api.dto.event_dto import CreateEventReq, ExtendedEvent
from app.data.domains.event import Event
from app.services.auth_service import AuthService
from app.services.event_service import EventService

router = APIRouter()


@router.get("/list-all", name="events:list-all")
async def list_all(
        event_service: Annotated[EventService, Depends(EventService)]
) -> List[Event]:
    return await event_service.get_all()


@router.get("/disciplines", name="events:disciplines")
async def list_all(
        event_service: Annotated[EventService, Depends(EventService)]
) -> List[str]:
    return await event_service.disciplines()


@router.get("/{event_id}", name="events:get-by-id")
async def get_by_id(
        event_id: str,
        event_service: Annotated[EventService, Depends(EventService)]
) -> Optional[ExtendedEvent]:
    return await event_service.get(event_id)


@router.post("", name="events:create")
async def create_event(
        user_id: Annotated[str, Depends(AuthService.require_user_id)],
        create_event_dto: Annotated[CreateEventReq, Body(...)],
        event_service: Annotated[EventService, Depends(EventService)]
) -> Event:
    return await event_service.create_event(user_id, create_event_dto)


@router.post("/search", name="events:search")
async def search(
        page: SearchReq,
        event_service: Annotated[EventService, Depends(EventService)]
) -> Page[ExtendedEvent]:
    return await event_service.search(page)


# todo: only for member
@router.put("/{event_id}", name="events:update")
async def update(
        event_id: str,
        updated_event: Annotated[CreateEventReq, Body(...)],
        event_service: Annotated[EventService, Depends(EventService)]
) -> bool:
    return await event_service.update(event_id, updated_event)
