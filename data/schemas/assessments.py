from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from data.models import AssessmentStatus


# Assessment Response (one Q&A pair)
class AssessmentResponseCreate(BaseModel):
    question_text: str = Field(..., min_length=1)
    answer_text: str = Field(..., min_length=1)
    trait_targeted: Optional[str] = None  # e.g. "openness"


class AssessmentResponseOut(AssessmentResponseCreate):
    id: UUID
    session_id: UUID
    answered_at: datetime

    model_config = {"from_attributes": True}

# Assessment Session
class AssessmentSessionCreate(BaseModel):
    user_id: UUID


class AssessmentSessionUpdate(BaseModel):
    status: Optional[AssessmentStatus] = None
    scorecard: Optional[dict] = None
    completed_at: Optional[datetime] = None


class AssessmentSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: AssessmentStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    scorecard: Optional[dict] = None
    responses: List[AssessmentResponseOut] = []

    model_config = {"from_attributes": True}