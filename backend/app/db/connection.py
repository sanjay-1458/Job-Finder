from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from app.config.settings import (
    DATABASE_URL
)

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True
    )
except Exception:
    engine = None

try:
    AsyncSessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False
    )
except Exception:
    AsyncSessionLocal = None