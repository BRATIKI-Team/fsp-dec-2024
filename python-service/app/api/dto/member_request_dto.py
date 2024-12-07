from typing import Optional

from pydantic import BaseModel


class SendMemberRequestResult(BaseModel):
    error: Optional[str] = None
