from typing import Annotated

from fastapi import Depends

from app.api.dto.event_request_dto import EventRequestDto
from app.api.dto.member_request_dto import ExtendedMemberRequest
from app.data.domains.event_request import EventRequest
from app.data.domains.member_request import MemberRequest
from app.services.event_service import EventService
from app.services.region_service import RegionService
from app.services.user_service import UserService


class EventRequestMapper:
    def __init__(
            self,
            region_service: Annotated[RegionService, Depends(RegionService)],
            event_service: Annotated[EventService, Depends(EventService)],
    ):
        self._region_service = region_service
        self._event_service = event_service

    async def map_req_to_extend(self, req: EventRequest) -> EventRequestDto:
        event = await self._event_service.get(req.event_id)
        region = await self._region_service.get(req.region_id)

        return EventRequestDto(
            id=req.id,
            region_id=req.region_id,
            event_id=req.event_id,
            event=event,
            region=region,
            status=req.status,
        )
