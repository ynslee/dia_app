from datetime import datetime, timezone
import enum

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

try:
    from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
    JSONType = JSONB
except Exception:
    from sqlalchemy import JSON as JSONType  # type: ignore

# Enums
class Gender(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    undisclosed = "undisclosed"

class DiabetesType(str, enum.Enum):
    none = "none"
    prediabetic = "prediabetic"
    type1 = "type1"
    ype2 = "type2"
    gdm = "gestational diabetes"

#should this be just metric/imperial
class Units(str, enum.Enum):
    metric = "metric"
    imperial = "imperial"

class BGUnits(str, enum.Enum):
	mmol = "mmol/L"
	mg = "mg/dL"

# Tables
class User(Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)

	# this is not done in hash. Just writing this as column optional for future and so I need to remember.
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

	#uselist=False means one-to-one relationship
    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings: Mapped["AccountSettings"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)

    first_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    age: Mapped[int | None] = mapped_column(nullable=True)
    height_cm: Mapped[int | None] = mapped_column(nullable=True)
    gender: Mapped[Gender] = mapped_column(SAEnum(Gender, native_enum=False), default=Gender.undisclosed)
    diabetes_type: Mapped[DiabetesType] = mapped_column(SAEnum(DiabetesType, native_enum=False), default=DiabetesType.none)

    user: Mapped["User"] = relationship(back_populates="profile")

class AccountSettings(Base):
    __tablename__ = "account_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)

    dark_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    email_notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    push_notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    preferred_units: Mapped[Units] = mapped_column(SAEnum(Units, native_enum=False), default=Units.metric)
    preferred_units_BG: Mapped[BGUnits] = mapped_column(SAEnum(BGUnits, native_enum=False), default=Units.mmol)

    checklist: Mapped[dict] = mapped_column(JSONType, default=dict)

    user: Mapped["User"] = relationship(back_populates="settings")

# Indexes
Index("ix_profile_user", Profile.user_id)
Index("ix_settings_user", AccountSettings.user_id)


#gotta use Base.metadata.create_all(engine) to create all metadatas in the main file
