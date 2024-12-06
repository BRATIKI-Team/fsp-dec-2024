from typing import Annotated, List

from fastapi import Depends
from fastapi_mail import MessageSchema, MessageType

from app.api.dto.event_request_dto import SendRequestResult
from app.core.config import APP_NAME
from app.data.domains.event import Event
from app.data.domains.event_request import EventRequest, EventRequestStatus
from app.data.repositories.event_request_repository import EventRequestRepository
from app.services.base_service import BaseService
from app.services.event_service import EventService
from app.services.user_service import UserService


class EventRequestService(BaseService[EventRequest]):
    def __init__(
            self,
            user_service: Annotated[UserService, Depends(UserService)],
            event_service: Annotated[EventService, Depends(EventService)],
            event_request_repository: Annotated[EventRequestRepository, Depends(EventRequestRepository)]):
        super().__init__(event_request_repository)
        self._user_service = user_service
        self._event_service = event_service
        self._event_request_repository = event_request_repository

    async def set_status(self, request_id: str, event_request: EventRequest) -> bool:
        event = await self._event_service.get(event_request.event_id)
        if event is None:
            raise Exception("Event is not found")

        user = await self._user_service.get(event.member_created_id)
        if user is None:
            raise Exception("User is not found")

        match event_request.status:
            case EventRequestStatus.ACCEPTED:
                print("accepted")
                # await self.notify_about_accepted_request(user.email, event, event_request)
            case EventRequestStatus.DECLINED:
                print("declined")
                #await self.notify_about_declined_request(user.email, event, event_request)

        return await super().update(request_id, event_request)

    async def send_event_request(self, event_id: str) -> SendRequestResult:
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
            return SendRequestResult(error="request-already-exists")

        event_request_id = await super().create(event_request)
        if event_request_id is None:
            return SendRequestResult(error="something-went-wrong")

        return SendRequestResult()

    async def get_by_region_id(self, region_id: str) -> List[EventRequest]:
        filters = {"region_id": region_id}
        return await super().filter(filters)

    async def notify_about_declined_request(self, user_email: str, event: Event, event_req: EventRequest) -> None:
        email_body = {
            "company_name": APP_NAME,
            "event_name": event.name
        }

        email_message = MessageSchema(
            subject="Отклонение заявки.",
            recipients=[user_email],
            template_body=email_body,
            subtype=MessageType.html
        )
        #await self._mail.send_message(email_message)

    async def notify_about_accepted_request(self, user_email: str, event: Event, event_req: EventRequest):
        # todo
        pass