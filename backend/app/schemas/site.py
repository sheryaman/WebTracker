from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import datetime

class WebSiteBase(BaseModel):
    name: str
    url: str

class WebSiteCreate(WebSiteBase):
    check_interval: Optional[int] = 60

class WebSiteResponse(WebSiteBase):
    id: int
    is_active: bool
    created_at: datetime
    last_status: Optional[int] = None
    latency: Optional[float] = None
    
    model_config = {"from_attributes": True}