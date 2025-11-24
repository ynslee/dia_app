from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
    )
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, utcnow

try:
    from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
    JSONType = JSONB
except Exception:
    from sqlalchemy import JSON as JSONType  # type: ignore


# Tables
class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
        )
    # TODO: should these be nullable or not show them depending on settings?
    carbs: Mapped[int] = mapped_column(Integer, nullable=True)
    protein: Mapped[int] = mapped_column(Integer, nullable=True)
    fat: Mapped[int] = mapped_column(Integer, nullable=True)
    calories: Mapped[int] = mapped_column(Integer, nullable=True)
    foods: Mapped[dict] = mapped_column(JSONType, default=dict)
    time_of_meal: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False
        )
    # TODO decide on GI score metric


class Meal_Settings(Base):
    __tablename__ = "meal_settings"

    id = Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
        )
    schedule: Mapped[dict] = mapped_column(JSONType, default=dict)
    # TODO why did we have the is_active? for notifications?
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    show_calories: Mapped[bool] = mapped_column(Boolean, default=True)


class Meal_Images(Base):
    __tablename__ = "meal_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"),
        index=True
        )
    image_url: Mapped[str] = mapped_column(String(2000), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=True)
    is_thumbnail: Mapped[bool] = mapped_column(Boolean, default=False)
    # TODO: json list of detected foods when feature is developed
