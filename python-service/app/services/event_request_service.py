from typing import Annotated, List

from fastapi import Depends

from app.api.dto.event_request_dto import SendEventRequestResult
from app.data.domains.event import Event
from app.data.domains.event_request import EventRequest, EventRequestStatus
from app.data.repositories.event_request_repository import EventRequestRepository
from app.services.base_service import BaseService
from app.services.event_service import EventService
from app.services.mail.mail_service import MailService
from app.services.user_service import UserService


class EventRequestService(BaseService[EventRequest]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            event_service: Annotated[EventService, Depends(EventService)],
            event_request_repository: Annotated[EventRequestRepository, Depends(EventRequestRepository)],
            mail_service: Annotated[MailService, Depends(MailService)]):
        super().__init__(event_request_repository)
        self._user_service = user_service
        self._event_service = event_service
        self._event_request_repository = event_request_repository
        self._mail_service = mail_service

    async def set_status(self, request_id: str, event_request: EventRequest) -> bool:
        event = await self._event_service.get(event_request.event_id)
        if event is None:
            raise Exception("Event is not found")

        user = await self._user_service.get(event.member_created_id)
        if user is None:
            raise Exception("User is not found")

        match event_request.status:
            case EventRequestStatus.APPROVED:
                print("approved")
                event.is_approved_event = True
                updated = await self._event_service.update(event.id, event)
                print(updated, event)
                await self._mail_service.notify_about_declined_request(user.email, event, event_request)
            case EventRequestStatus.DECLINED:
                print("declined")
                await self._mail_service.notify_about_declined_request(user.email, event, event_request)

        return await super().update(request_id, event_request)

    async def send_event_request(self, event_id: str) -> SendEventRequestResult:
        event = await self._event_service.get(event_id)
        if event is None:
            raise Exception("Event is not found")
        event_request = EventRequest(
            event_id=event.id,
            region_id=event.region_id,
            status=EventRequestStatus.PENDING
        )

        existing_reqeust = await super().filter({"event_id": event_id})
        if len(existing_reqeust):
            return SendEventRequestResult(error="request-already-exists")

        event_request_id = await super().create(event_request)
        if event_request_id is None:
            return SendEventRequestResult(error="something-went-wrong")

        return SendEventRequestResult()

    async def get_by_region_id(self, region_id: str) -> List[EventRequest]:
        filters = {"region_id": region_id}
        return await super().filter(filters)

    async def get_by_event_id(self, event_id: str) -> EventRequest:
        filters = {"event_id": event_id}
        return (await super().filter(filters))[0]
