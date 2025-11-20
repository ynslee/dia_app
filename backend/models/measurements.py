"""Database models for measurements."""
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import (
    Enum as SAEnum,
    Float,
    String,
    DateTime,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from db import Base, utcnow


# Enums
class MeasurementType(str, Enum):
    """
    MeasurementType class is an Enum of accepted measurements to validate
    incoming requests.
    """

    BLOOD_PRESSURE = "bp"
    HEART_RATE = "hr"
    BLOOD_SUGAR = "bs"
    HEIGHT = "ht"
    WEIGHT = "wt"


# Constants

MAX_DEVICE_NAME = 100
MAX_NOTE_LENGTH = 200


# Tables
class Measurement(Base):
    """
    Measurement model sets up the measurement table using sqlalchemy.
    """
    __tablename__ = "measurements"
    # table args for stuff like foreign keys, unique constraints, autoload...
    # __table_args__ = ()

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    measurement_type: Mapped[MeasurementType] = mapped_column(
        SAEnum(MeasurementType)
        )
    value_1: Mapped[float] = mapped_column(Float, nullable=False)
    value_2: Mapped[float] = mapped_column(Float, nullable=True)
    source: Mapped[str] = mapped_column(
        String(MAX_DEVICE_NAME),
        nullable=True
        )
    time_taken: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False)
    note: Mapped[str] = mapped_column(
        String(MAX_NOTE_LENGTH),
        nullable=True
        )
    symptoms: Mapped[str] = mapped_column(
        String(MAX_NOTE_LENGTH),
        nullable=True
        )
    # TODO: make sure this is the users table/ fk to use
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    # TODO: wait and see if relationship needs to be setup
