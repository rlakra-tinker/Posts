#
# Author: Rohtash Lakra
#
import os
from asyncio import current_task
from collections.abc import AsyncIterator

from sqlalchemy import SC
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from framework.enums import EnvType


class AsyncSessionManager:
    """Creates an AsyncSession and managing its lifecycle using the asyncio module, along with demonstrating the use
    of dependency injection for cleaner and more maintainable code.
    """

    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker = None
        self.session = None

    def init_db(self):
        # Database connection parameters...
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.DEFAULT_POOL_SIZE = int(os.getenv("DEFAULT_POOL_SIZE", 1))
        self.RDS_POOL_SIZE = int(os.getenv("RDS_POOL_SIZE", 1))
        self.AUTO_COMMIT = EnvType.getenv_bool(os.getenv("AUTO_COMMIT", False))

        self.RDS_POOL_SIZE += self.DEFAULT_POOL_SIZE
        # validate the pool size
        if (self.RDS_POOL_SIZE - self.DEFAULT_POOL_SIZE) < 1:
            raise Exception('PoolSize should be higher that 0!')

        # Creating an asynchronous engine
        self.engine = create_async_engine(
            self.DATABASE_URL,
            pool_size=self.RDS_POOL_SIZE,
            max_overflow=0,
            pool_pre_ping=False,
            echo=True
        )

        # Creating an asynchronous session class
        self.session_maker = async_sessionmaker(
            autocommit=self.AUTO_COMMIT, autoflush=False, bind=self.engine
        )

        # Creating a scoped session
        self.session = async_scoped_session(self.session_maker, scopefunc=current_task)

    async def close(self):
        """Closing the database session."""
        if self.engine is None:
            raise Exception("DatabaseSessionManager is not initialized!")

        await self.engine.dispose()

    async def getDatabase(self) -> AsyncIterator[AsyncSession]:
        """Initialize and close the database session properly. It ensures that we have a valid and scoped database
        session for each request.
        """
        session = self.session()
        if session is None:
            raise Exception("DatabaseSessionManager is not initialized")

        try:
            # Setting the search path and yielding the session...
            # TODO: FIX ME
            # await session.execute(
            #     text(f"SET search_path TO {SCHEMA}")
            # )
            yield session

        except Exception:
            await session.rollback()
            raise
        finally:
            # Closing the session after use...
            await session.close()


# Note: - move to middleware
# Initialize the DatabaseSessionManager
sessionManager = AsyncSessionManager()


async def getDatabase() -> AsyncIterator[AsyncSession]:
    return sessionManager.getDatabase()
