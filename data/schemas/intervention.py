from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from data.models import InterventionSeverity

class InterventionBase(BaseModel):
    trigger_reason: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    severity: InterventionSeverity = InterventionSeverity.LOW


class InterventionCreate(InterventionBase):
    user_id: UUID


class InterventionUpdate(BaseModel):
    acknowledged_at: Optional[datetime] = None

class InterventionResponse(InterventionBase):
    id: UUID
    user_id: UUID
    sent_at: datetime
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}