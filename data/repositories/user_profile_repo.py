from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from data.models import UserProfile
from data.schemas.user_profile import UserProfileCreate, UserProfileUpdate


async def create_user(db: AsyncSession, data: UserProfileCreate) -> UserProfile:
    """Insert a new user profile into the DB."""
    user = UserProfile(**data.model_dump())
    db.add(user)
    await db.flush()        # writes to DB but doesn't commit yet
    await db.refresh(user)  # reloads from DB to get server-generated fields (id, created_at)
    return user


async def get_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[UserProfile]:
    """Fetch a single user by their UUID. Returns None if not found."""
    result = await db.execute(
        select(UserProfile).where(UserProfile.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserProfile]:
    """Fetch a user by email. Used for uniqueness checks."""
    result = await db.execute(
        select(UserProfile).where(UserProfile.email == email)
    )
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession) -> List[UserProfile]:
    """Fetch all users. Admin use only."""
    result = await db.execute(select(UserProfile))
    return list(result.scalars().all())


async def update_user(
    db: AsyncSession,
    user_id: UUID,
    data: UserProfileUpdate
) -> Optional[UserProfile]:
    """
    Update a user's fields. Only updates fields that were actually provided
    (exclude_unset=True skips fields the client didn't send).
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:
    """Delete a user. Returns True if deleted, False if not found."""
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.flush()
    return True