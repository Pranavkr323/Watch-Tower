from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from datetime import datetime
from decimal import Decimal
from app.enums import Status

class MonitorCreate(BaseModel):
    product_link: HttpUrl = Field(...)
    threshold: Decimal = Field(..., gt=0, decimal_places=2)

class MonitorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    monitor_id: int
    threshold: Decimal
    Product_link: HttpUrl
    created_at: datetime
    updated_at: datetime
    status: Status
