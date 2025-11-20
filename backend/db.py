#this is like a database helper
from datetime import datetime, timezone
from typing import Any
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

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