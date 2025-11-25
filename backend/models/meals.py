from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SAEnum,
    ARRAY,
    )
from sqlalchemy.orm import Mapped, mapped_column

from db import Base, utcnow

try:
    from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
    JSONType = JSONB
except Exception:
    from sqlalchemy import JSON as JSONType  # type: ignore


class MealType(str, Enum):
    """
    MealType class is an Enum of meal types to validate
    incoming requests.
    """

    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    UNSPECIFIED = "unspecified"


class Location(str, Enum):
    """
    Location class is an Enum of locations meals were consumed to validate
    incoming requests.
    """

    HOME = "home"
    RESTAURAUNT = "restauraunt"
    UNSPECIFIED = "unspecified"
    # TODO: consider other locations


class Food_Units(str, Enum):
    """
    Food_Units class is an Enum of units food portions are reported in to
    validateincoming requests.
    """

    GRAMS = "grams"
    CUPS = "cups"
    SERVINGS = "servings"
    OUNCES = "ounces"
    # TODO: consider other locations


# Constants

MAX_NOTE_LENGTH = 200
MAX_IMAGE_HASH = 1000


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
    note: Mapped[str] = mapped_column(
        String(MAX_NOTE_LENGTH),
        nullable=True
        )
    meal_type: Mapped[MealType] = mapped_column(
        SAEnum(MealType),
        nullable=False,
        default=MealType.UNSPECIFIED
        )
    location: Mapped[Location] = mapped_column(
        SAEnum(Location),
        nullable=False,
        default=Location.UNSPECIFIED
        )
    # TODO: consider columns: verified vs estimated macros,
    # is_manual, confidence score if is ML related


class Meal_Settings(Base):
    __tablename__ = "meal_settings"

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

    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"),
        index=True
        )
    image_url: Mapped[str] = mapped_column(String(2000), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=True)
    is_thumbnail: Mapped[bool] = mapped_column(Boolean, default=False)
    metadata: Mapped[dict] = mapped_column(JSONType, default=dict)
    image_hash: Mapped[str] = mapped_column(
        String(MAX_IMAGE_HASH),
        nullable=False
        )
    # TODO: json list of detected foods when feature is developed


class Foods(Base):
    __tablename__ = "foods"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    serving_size_grams: Mapped[int] = mapped_column(Integer)
    calories_per_100_grams: Mapped[int] = mapped_column(Integer)
    carbohydrates_per_100_grams: Mapped[int] = mapped_column(Integer)
    fat_per_100_grams: Mapped[int] = mapped_column(Integer)
    protein_per_100_grams: Mapped[int] = mapped_column(Integer)
    micronutrients: Mapped[dict] = mapped_column(JSONType, default=dict)
    ingredients: Mapped[list[str]] = mapped_column(ARRAY(String))


class Meal_Foods(Base):
    __tablename__ = "meal_foods"

    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    food_id: Mapped[int] = mapped_column(
        ForeignKey("foods.id", ondelete="CASCADE"),
        nullable=False,
        index=True
        )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    units: Mapped[Food_Units] = mapped_column(
        SAEnum(Food_Units),
        default=Food_Units.GRAMS
        )

# TODO consider if we want tags for the meals.
