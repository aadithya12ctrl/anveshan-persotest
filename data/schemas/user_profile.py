
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    age: Optional[int] = Field(None, ge=1, le=120)
    email: Optional[EmailStr] = None


class UserProfileCreate(UserProfileBase):
    pass  # same as Base for now — no extra fields needed on create


class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    age: Optional[int] = Field(None, ge=1, le=120)
    email: Optional[EmailStr] = None
    big_five_scores: Optional[dict] = None
    procrastination_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    productivity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_assessment_complete: Optional[bool] = None


class UserProfileResponse(UserProfileBase):
    id: UUID
    big_five_scores: Optional[dict] = None
    procrastination_score: Optional[float] = None
    productivity_score: Optional[float] = None
    is_assessment_complete: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # allows converting SQLAlchemy model → this schema