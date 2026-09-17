from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from datetime import datetime
from decimal import Decimal
from app.enums import Status


class CreateMonitor(BaseModel):
    product_link: HttpUrl = Field(...)
    threshold: Decimal = Field(..., gt=0, decimal_places=2)


class MonitorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    monitor_id: int
    threshold: Decimal
    product_link: HttpUrl
    created_at: datetime
    updated_at: datetime
    status: Status

class UpdateMonitor(BaseModel):
    threshold: Decimal | None = Field(default=None,
                                       gt=0,
                                       decimal_places=2)
    product_link: HttpUrl | None = None

