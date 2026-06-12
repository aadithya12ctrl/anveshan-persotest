from uuid import UUID
from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from data.models import ScreentimeEntry
from data.schemas.screentime import ScreentimeEntryCreate


async def add_entry(
    db: AsyncSession,
    data: ScreentimeEntryCreate
) -> ScreentimeEntry:
    """Log a single screentime entry."""
    entry = ScreentimeEntry(**data.model_dump())
    db.add(entry)
    await db.flush()
    await db.refresh(entry)
    return entry


async def get_entries_by_user(
    db: AsyncSession,
    user_id: UUID
) -> List[ScreentimeEntry]:
    """Fetch all screentime entries for a user, newest first."""
    result = await db.execute(
        select(ScreentimeEntry)
        .where(ScreentimeEntry.user_id == user_id)
        .order_by(ScreentimeEntry.recorded_at.desc())
    )
    return list(result.scalars().all())


async def get_entries_by_date_range(
    db: AsyncSession,
    user_id: UUID,
    start: datetime,
    end: datetime
) -> List[ScreentimeEntry]:
    """Fetch entries for a user within a specific date range."""
    result = await db.execute(
        select(ScreentimeEntry)
        .where(
            ScreentimeEntry.user_id == user_id,
            ScreentimeEntry.recorded_at >= start,
            ScreentimeEntry.recorded_at <= end,
        )
        .order_by(ScreentimeEntry.recorded_at.asc())
    )
    return list(result.scalars().all())


async def get_daily_summary(
    db: AsyncSession,
    user_id: UUID,
    date: datetime
) -> List[dict]:
    """
    Aggregate screentime by app for a specific day.
    Returns a list of { app_name, category, total_seconds, entry_count }.
    Uses SQL GROUP BY under the hood.
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

    result = await db.execute(
        select(
            ScreentimeEntry.app_name,
            ScreentimeEntry.category,
            func.sum(ScreentimeEntry.duration_seconds).label("total_seconds"),
            func.count(ScreentimeEntry.id).label("entry_count"),
        )
        .where(
            ScreentimeEntry.user_id == user_id,
            ScreentimeEntry.recorded_at >= start,
            ScreentimeEntry.recorded_at <= end,
        )
        .group_by(ScreentimeEntry.app_name, ScreentimeEntry.category)
        .order_by(func.sum(ScreentimeEntry.duration_seconds).desc())
    )

    return [
        {
            "app_name": row.app_name,
            "category": row.category,
            "total_seconds": row.total_seconds,
            "entry_count": row.entry_count,
        }
        for row in result.all()
    ]


async def delete_entries_older_than(
    db: AsyncSession,
    user_id: UUID,
    before: datetime
) -> int:
    """
    Delete old screentime entries to save space.
    Returns count of deleted rows.
    """
    result = await db.execute(
        delete(ScreentimeEntry)
        .where(
            ScreentimeEntry.user_id == user_id,
            ScreentimeEntry.recorded_at < before,
        )
    )
    await db.flush()
    return result.rowcount