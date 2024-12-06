from datetime import datetime
from typing import Optional

from onnxruntime.transformers.models.stable_diffusion.diffusion_models import BaseModel

class Event(BaseModel):
    id: Optional[str] = None
    regionId: str
    name: str
    description: str
    datetime: datetime