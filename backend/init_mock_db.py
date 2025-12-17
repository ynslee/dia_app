from db import Base, engine
import asyncio
from sqlalchemy import text
from models import account, measurements
# noqa: F401  - just to register models


async def init_db() -> None:
    """
    Initialize the database schema using AsyncEngine.
    disable foreign keys
    drop and create all tables 
    re-enable foreign keys
    """

    print("removing")
    async with engine.begin() as conn:
        await conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        print("  Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)

        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

        await conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

        print("✅ Mock DB schema initialization complete.")


if __name__ == "__main__":
    asyncio.run(init_db())