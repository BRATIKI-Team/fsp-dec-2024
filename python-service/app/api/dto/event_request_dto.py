from typing import Optional

from pydantic import BaseModel

class SendRequestResult(BaseModel):
    error: Optional[str]