from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
from data.models import Base


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,        # logs all SQL in dev, silent in prod
    pool_pre_ping=True,         # checks connection health before using it
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # keeps objects usable after commit
)


async def get_db() -> AsyncSession:

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Creates all tables defined in models.py.
    Call this in your FastAPI lifespan startup event.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)