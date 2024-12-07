from typing import Optional

from pydantic import BaseModel

class SendEventRequestResult(BaseModel):
    error: Optional[str] = None