from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from data.models import AppCategory


class ScreentimeEntryBase(BaseModel):
    app_name: str = Field(..., min_length=1, max_length=255)
    category: AppCategory = AppCategory.OTHER
    duration_seconds: int = Field(..., gt=0)
    recorded_at: datetime


class ScreentimeEntryCreate(ScreentimeEntryBase):
    user_id: UUID

class ScreentimeEntryResponse(ScreentimeEntryBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class AppUsageSummary(BaseModel):
    app_name: str
    category: AppCategory
    total_seconds: int
    entry_count: int


class ScreentimeDailySummary(BaseModel):
    user_id: UUID
    date: datetime
    total_seconds: int
    by_app: List[AppUsageSummary]