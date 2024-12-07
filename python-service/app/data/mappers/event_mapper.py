from typing import Annotated

from fastapi import Depends

from app.api.dto.event_dto import ExtendedEvent
from app.data.domains.event import Event
from app.services.event_request_service import EventRequestService
from app.services.file_model_service import FileModelService
from app.services.region_service import RegionService
from app.services.user_service import UserService


class EventMapper:
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            region_service: Annotated[RegionService, Depends(RegionService)],
            file_service: Annotated[FileModelService, Depends(FileModelService)],
            request_service: Annotated[EventRequestService, Depends(EventRequestService)]
    ):
        self._user_service = user_service
        self._region_service = region_service
        self._file_service = file_service
        self._request_service = request_service

    async def map_event_to_extend(self, event: Event) -> ExtendedEvent:
        user = await self._user_service.get(event.member_created_id)
        region = await self._region_service.get(event.region_id)
        request = await self._request_service.get_by_event_id(event.id)

        documents = [doc.get_dto() for doc in
                     await self._file_service.get_many(event.documents_ids)] if event.documents_ids else []
        protocols = [doc.get_dto() for doc in
                     await self._file_service.get_many(event.protocols_ids)] if event.protocols_ids else []
        result = (await self._file_service.get(event.result_file_id)).get_dto() if event.result_file_id else None
        results = [result] if result else []

        return ExtendedEvent(
            user=user,
            event=event,
            region=region,
            documents=documents,
            protocols=protocols,
            request=request,
            results=results
        )
