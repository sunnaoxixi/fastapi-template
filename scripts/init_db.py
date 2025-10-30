import asyncio
import sys

from alembic import command
from alembic.config import Config
from loguru import logger

from src.contexts.shared.infrastructure.persistence.database import init_db
from src.settings import settings


async def main() -> None:
    logger.info("🔍 Checking database connection...")
    try:
        await init_db()
        logger.info("✅ Database connection successful!")
    except Exception:
        logger.exception("❌ Database connection failed")
        sys.exit(1)

    logger.info("\n🔄 Running database migrations...")

    try:
        alembic_cfg = Config("alembic.ini")

        alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)

        command.upgrade(alembic_cfg, "head")

        logger.info("✅ Database migrations completed successfully!")
    except Exception:
        logger.exception("❌ Database migrations failed")
        sys.exit(1)

    logger.info("\n🎉 Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())
