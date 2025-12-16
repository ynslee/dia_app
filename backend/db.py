#this is like a database helper
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
import os

#TO DO: this is leaving space for normal dev to use SQLite.
#    - If DATABASE_URL is set in environment, use that.
#    - Otherwise, default to a local SQLite file (dev.db).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./dev.db",  # fallback for dev
)
def utcnow() -> datetime:
    return datetime.now(timezone.utc)

#it is better to have one central place(base) to have all the meta data
class Base(DeclarativeBase):

	id: Mapped[int] = mapped_column(primary_key=True)

	created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
    )
	updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
    )
	#for debugging or logging
	def as_dict(self) -> dict[str, Any]:
		#for each column(c)
		return {c.key: getattr(self, c.key) for c in self.__table__.columns}
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} id={getattr(self, 'id', None)!r}>"

engine = create_engine(
    DATABASE_URL,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    """FastAPI dependency: yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()