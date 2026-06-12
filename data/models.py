import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean,
    DateTime, ForeignKey, Text, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
import enum

class Base(DeclarativeBase):
    pass


class AssessmentStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class InterventionSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AppCategory(str, enum.Enum):
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    PRODUCTIVITY = "productivity"
    COMMUNICATION = "communication"
    GAMING = "gaming"
    OTHER = "other"

# Mixin — adds created_at and updated_at to any model

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# Models
class UserProfile(TimestampMixin, Base):

    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String(255), unique=True, nullable=True)

    # Big Five personality scores stored as JSON
    # { openness, conscientiousness, extraversion, agreeableness, neuroticism }
    big_five_scores = Column(JSONB, nullable=True, default=dict)

    procrastination_score = Column(Float, nullable=True)   # 0.0 to 1.0
    productivity_score = Column(Float, nullable=True)      # 0.0 to 1.0

    is_assessment_complete = Column(Boolean, default=False, nullable=False)

    # Relationships
    screentime_entries = relationship("ScreentimeEntry", back_populates="user", cascade="all, delete-orphan")
    assessment_sessions = relationship("AssessmentSession", back_populates="user", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="user", cascade="all, delete-orphan")
    session_histories = relationship("SessionHistory", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserProfile id={self.id} name={self.name}>"


class ScreentimeEntry(TimestampMixin, Base):

    __tablename__ = "screentime_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)

    app_name = Column(String(255), nullable=False)
    category = Column(SAEnum(AppCategory), nullable=False, default=AppCategory.OTHER)
    duration_seconds = Column(Integer, nullable=False)   # how long the app was used
    recorded_at = Column(DateTime(timezone=True), nullable=False)  # when this usage happened

    # Relationships
    user = relationship("UserProfile", back_populates="screentime_entries")

    def __repr__(self):
        return f"<ScreentimeEntry user={self.user_id} app={self.app_name} duration={self.duration_seconds}s>"


class AssessmentSession(TimestampMixin, Base):

    __tablename__ = "assessment_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)

    status = Column(SAEnum(AssessmentStatus), nullable=False, default=AssessmentStatus.IN_PROGRESS)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Scorecard output — stored as JSON once assessment is complete
    scorecard = Column(JSONB, nullable=True)

    # Relationships
    user = relationship("UserProfile", back_populates="assessment_sessions")
    responses = relationship("AssessmentResponse", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AssessmentSession id={self.id} user={self.user_id} status={self.status}>"


class AssessmentResponse(TimestampMixin, Base):

    __tablename__ = "assessment_responses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id"), nullable=False)

    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    trait_targeted = Column(String(100), nullable=True)   # e.g. "openness", "conscientiousness"
    answered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    session = relationship("AssessmentSession", back_populates="responses")

    def __repr__(self):
        return f"<AssessmentResponse session={self.session_id} trait={self.trait_targeted}>"


class Intervention(TimestampMixin, Base):

    __tablename__ = "interventions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)

    trigger_reason = Column(Text, nullable=False)   # e.g. "Instagram usage 2x above baseline"
    message = Column(Text, nullable=False)           # the actual nudge text
    severity = Column(SAEnum(InterventionSeverity), nullable=False, default=InterventionSeverity.LOW)

    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)  # null = not yet seen

    # Relationships
    user = relationship("UserProfile", back_populates="interventions")

    def __repr__(self):
        return f"<Intervention user={self.user_id} severity={self.severity}>"


class SessionHistory(TimestampMixin, Base):

    __tablename__ = "session_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id"), nullable=False)

    role = Column(String(50), nullable=False)       # 'user' or 'assistant'
    content = Column(Text, nullable=False)           # the message text
    message_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Optional: link to an assessment session if this message was part of one
    assessment_session_id = Column(UUID(as_uuid=True), ForeignKey("assessment_sessions.id"), nullable=True)

    # Relationships
    user = relationship("UserProfile", back_populates="session_histories")

    def __repr__(self):
        return f"<SessionHistory user={self.user_id} role={self.role}>"