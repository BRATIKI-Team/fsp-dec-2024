from typing import Annotated

from fastapi import Depends

from app.data.domains.user import User
from app.data.repositories.event_repository import EventRepository
from app.services.base_service import BaseService

class EventService(BaseService[User]):
    def __init__(self, event_repository: Annotated[EventRepository, Depends(EventRepository)]):
        super().__init__(event_repository)
        self.event_repository = event_repository

