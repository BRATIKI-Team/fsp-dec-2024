from typing import Annotated

from fastapi import Depends
from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import Template

from app.core.dependencies import get_mail
from app.data.domains.event import Event
from app.data.domains.event_request import EventRequest

class MailService:
    def __init__(self, mail: Annotated[FastMail, Depends(get_mail)]):
        self._mail = mail

    async def notify_about_declined_request(
            self,
            user_email: str,
            event: Event,
            event_req: EventRequest
    ) -> None:
        template_path = "app/services/mail/declined_request_notification.html"
        with open(template_path, "r", encoding="utf-8") as file:
            html_template = file.read()

        template = Template(html_template)
        html_body = template.render(
            event_name=event.name,
            event_datetime=event.datetime.strftime('%Y-%m-%d %H:%M'),
            event_region=event.region_id,
            canceled_reason=event_req.canceled_reason or "No reason provided."
        )
        print(html_body)
        subject = f"Уведомление об изменении статуса Вашей заявки"
        message = MessageSchema(
            subject=subject,
            recipients=["artush.baghdasaryan@mail.ru"],
            body=html_body,
            subtype=MessageType.html
        )
        print("message", message)
        await self._mail.send_message(message)

    async def notify_about_approved_request(
            self,
            user_email: str,
            event: Event,
            event_req: EventRequest
    ) -> None:
        template_path = "approved_request_notification.html"
        with open(template_path, "r", encoding="utf-8") as file:
            html_template = file.read()

        template = Template(html_template)
        html_body = template.render(
            event_name=event.name,
            event_datetime=event.datetime.strftime('%Y-%m-%d %H:%M'),
            event_region=event.region_id,
            canceled_reason=event_req.canceled_reason or "No reason provided."
        )

        subject = f"Уведомление об изменении статуса Вашей заявки"
        message = MessageSchema(
            subject=subject,
            recipients=[user_email],
            body=html_body,
            subtype=MessageType.html
        )

        await self._mail.send_message(message)
