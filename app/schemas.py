from pydantic import BaseModel
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str
    url: str

class ServiceCheck(BaseModel):
    checked_at: datetime
    reachable: bool 
    status_code: int | None
    response_time: float | None

    model_config = {"from_attributes": True}

