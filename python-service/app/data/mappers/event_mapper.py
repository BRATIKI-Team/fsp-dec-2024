from typing import Annotated, List

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
            results=results,
            is_approved_event=event.is_approved_event
        )

    async def map_events_to_extend(self, events: List[Event]) -> List[ExtendedEvent]:
        """To avoid N+1"""
        user_ids: List[str] = []
        region_ids: List[str] = []
        file_ids: List[str] = []

        for event in events:
            region_ids.append(event.region_id)
            if event.member_created_id:
                user_ids.append(event.member_created_id)
            if event.documents_ids:
                file_ids.append(*event.documents_ids)
            if event.protocols_ids:
                file_ids.append(*event.protocols_ids)
            if event.result_file_id:
                file_ids.append(event.result_file_id)

        users = await self._user_service.get_many(user_ids)
        regions = await self._region_service.get_many(region_ids)
        files = await self._file_service.get_many(file_ids)

        extended_events = []
        for event in events:
            request = await self._request_service.get_by_event_id(event.id)

            extended_events.append(ExtendedEvent(
                event=event,
                region=next((region for region in regions if region.id == event.region_id), None),
                user=next((user for user in users if user.id == event.member_created_id), None),
                request=request,
                documents=[file.get_dto() for file in files if
                           file.id in (event.documents_ids if event.documents_ids else [])],
                protocols=[file.get_dto() for file in files if
                           file.id in (event.protocols_ids if event.protocols_ids else [])],
                results=[file.get_dto() for file in files if file.id == event.result_file_id],
                is_approved_event=event.is_approved_event
            ))

        return extended_events
