from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from data.models import AssessmentSession, AssessmentResponse, AssessmentStatus
from data.schemas.assessment import (
    AssessmentSessionCreate,
    AssessmentSessionUpdate,
    AssessmentResponseCreate,
)


async def create_session(
    db: AsyncSession,
    data: AssessmentSessionCreate
) -> AssessmentSession:
    """Start a new assessment session for a user."""
    session = AssessmentSession(**data.model_dump())
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def get_session_by_id(
    db: AsyncSession,
    session_id: UUID
) -> Optional[AssessmentSession]:
    """
    Fetch a session by ID, including all its responses.
    selectinload tells SQLAlchemy to also load the related responses
    in the same query (avoids N+1 query problem).
    """
    result = await db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.id == session_id)
        .options(selectinload(AssessmentSession.responses))
    )
    return result.scalar_one_or_none()


async def get_sessions_by_user(
    db: AsyncSession,
    user_id: UUID
) -> List[AssessmentSession]:
    """Fetch all assessment sessions for a user, newest first."""
    result = await db.execute(
        select(AssessmentSession)
        .where(AssessmentSession.user_id == user_id)
        .options(selectinload(AssessmentSession.responses))
        .order_by(AssessmentSession.started_at.desc())
    )
    return list(result.scalars().all())


async def update_session(
    db: AsyncSession,
    session_id: UUID,
    data: AssessmentSessionUpdate
) -> Optional[AssessmentSession]:
    """Update session status or attach a scorecard."""
    session = await get_session_by_id(db, session_id)
    if not session:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(session, field, value)

    await db.flush()
    await db.refresh(session)
    return session


async def add_response(
    db: AsyncSession,
    session_id: UUID,
    data: AssessmentResponseCreate
) -> AssessmentResponse:
    """Add a single Q&A response to an existing session."""
    response = AssessmentResponse(session_id=session_id, **data.model_dump())
    db.add(response)
    await db.flush()
    await db.refresh(response)
    return response


async def complete_session(
    db: AsyncSession,
    session_id: UUID,
    scorecard: dict
) -> Optional[AssessmentSession]:
    """Mark a session as complete and attach the scorecard."""
    from datetime import datetime, timezone
    return await update_session(
        db,
        session_id,
        AssessmentSessionUpdate(
            status=AssessmentStatus.COMPLETED,
            scorecard=scorecard,
            completed_at=datetime.now(timezone.utc)
        )
    )