from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from models.meals import MealType, Location, Food_Units


# ---------- MEAL SCHEMAS ----------

class MealBase(BaseModel):
    """
    MealBase class inherits from pydantic BaseModel and provides optional
    fields for request body related to meal api.
    """
    
    id: int | None = Field(
        default=None,
        description="ID of meal if already created",
        json_schema_extra={"example": "3"},
    )
    carbs: int | None = Field(
        default=None,
        ge=0,
        le=5000,
        description="Total carbs in grams",
        json_schema_extra={"example": "120"},
    )
    protein: int | None = Field(
        default=None,
        ge=0,
        le=5000,
        description="Total protein in grams",
        json_schema_extra={"example": "11"},
    )
    fat: int | None = Field(
        default=None,
        ge=0,
        le=5000,
        description="Total fat in grams",
        json_schema_extra={"example": "18"},
    )
    calories: int | None = Field(
        default=None,
        ge=0,
        le=5000,
        description="Total calories",
        json_schema_extra={"example": "450"},
    )
    # TODO decide how we want to handle foods with the photos and AI analysis
    foods: dict | None = Field(
        default=None,
        description="Structured foods payload for the meal",
        json_schema_extra={"example": {"items": []}},
    )
    time_of_meal: datetime | None = Field(
        default=None,
        description="UTC timestamp when the meal was eaten",
        json_schema_extra={"example": "2025-12-05T14:30:00Z"},
    )
    note: str | None = Field(
        default=None,
        max_length=200,
        description="User note (<=200 chars)",
        json_schema_extra={"example": "my note"},
    )
    meal_type: MealType | None = Field(
        default=MealType.UNSPECIFIED,
        description="Meal Type: breakfast, lunch, dinner, snack, unspecified",
        json_schema_extra={"example": "lunch"},
    )
    location: Location | None = Field(
        default=Location.UNSPECIFIED,
        description="Meal location: home, restaurant, unspecified",
        json_schema_extra={"example": "home"},
    )


# TODO what do we want to require for the meals?
class MealCreate(MealBase):
    """
    MealCreate class inherits from MealBase and maps to fields in POST request
    body for creation of new meal entry.
    """

    time_of_meal: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the meal was eaten",
        json_schema_extra={"example": "2025-12-05T14:30:00Z"},
    )
    meal_type: MealType = Field(
        default=MealType.UNSPECIFIED,
        description="Meal Type: breakfast, lunch, dinner, snack, unspecified",
        json_schema_extra={"example": "lunch"},
    )
    location: Location = Field(
        default=Location.UNSPECIFIED,
        description="Meal location: home, restaurant, unspecified",
        json_schema_extra={"example": "home"},
    )


class MealUpdate(MealBase):
    """
    MealUpdate class inherits from MealBase all optional fields and requires
    meal id  to be provided.
    """
    
    id: int = Field(
        default=...,
        description="ID of meal to update",
        json_schema_extra={"example": "3"},
    )


class MealRead(BaseModel):
    """
    MealRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """
    
    id: int = Field(default=..., description="Meal ID")
    user_id: int | None = Field(
        default=None,
        description="Owner user ID (if present in response)",
    )
    carbs: int | None = Field(default=None, description="Total carbs in grams")
    protein: int | None = Field(default=None, description="Total protein in grams")
    fat: int | None = Field(default=None, description="Total fat in grams")
    calories: int | None = Field(default=None, description="Total calories")
    foods: dict | None = Field(default=None, description="Structured foods payload")
    time_of_meal: datetime = Field(
        default=...,
        description="UTC timestamp when the meal was eaten",
    )
    note: str | None = Field(default=None, description="User note (<=200 chars)")
    meal_type: MealType = Field(
        default=...,
        description="Meal Type: breakfast, lunch, dinner, snack, unspecified",
    )
    location: Location = Field(
        default=...,
        description="Meal location: home, restaurant, unspecified",
    )
    created_at: datetime | None = Field(
        default=None,
        description="Created timestamp if tracked",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Updated timestamp if tracked",
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "MealRead",
            "examples": [
                {
                    "id": 1,
                    "user_id": 42,
                    "carbs": 30,
                    "protein": 15,
                    "fat": 16,
                    "calories": 398,
                    "foods": {"items": []},
                    "note": "user note",
                    "meal_type": "lunch",
                    "location": "home",
                    "time_of_meal": "2025-11-05T14:29:00Z",
                    "created_at": "2025-11-05T14:30:00Z",
                    "updated_at": None
                }
            ]
        }
    )


# ---------- MEAL SETTINGS SCHEMAS ----------

class MealSettingsBase(BaseModel):
    """
    MealSettingsBase class inherits from pydantic BaseModel and provides
    optional fields for request body related to meal settings api.
    """
    # TODO decide how we want to handle the schedule
    schedule: dict | None = Field(
        default=None,
        description="User meal schedule preferences",
        json_schema_extra={"example": {"mon": ["08:00", "12:00", "18:00"]}},
    )
    # TODO decide how we want to handle the is_active
    # is_active: bool | None = Field(
    #     default=None,
    #     description="what is this for?",
    #     json_schema_extra={"example": True},
    # )
    show_calories: bool | None = Field(
        default=None,
        description="Toggle calories visibility",
        json_schema_extra={"example": True},
    )
    reminder_time_before_min: int | None = Field(
        default=None,
        ge=0,
        le=60,
        description="Minutes before meal to send reminder",
        json_schema_extra={"example": 15},
    )

# TODO this is the same as MealSettings Base, do we need separate?
class MealSettingsUpdate(MealSettingsBase):
    """
    MealSettingsUpdate class inherits from MealSettingsBase all optional fields.
    """


class MealSettingsRead(BaseModel):
    """
    MealSettingsRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """
    
    schedule: dict | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    show_calories: bool | None = Field(default=None)
    reminder_time_before_min: int | None = Field(default=None)


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "MealSettingsRead",
            "examples": [
                {
                    "schedule": {"mon": ["08:00", "12:00"]},
                    "is_active": True,
                    "show_calories": True,
                    "reminder_time_before_min": 15
                }
            ]
        }
    )

# ---------- MEAL IMAGES SCHEMAS ----------

class MealImageBase(BaseModel):
    """
    MealImageBase class inherits from pydantic BaseModel and provides optional
    fields for request body related to meal image api.
    """
    
    meal_id: int | None = Field(
        default=None,
        description="Associated meal ID",
        json_schema_extra={"example": 1},
    )
    image_url: str | None = Field(
        default=None,
        description="Image URL",
        json_schema_extra={"example": "https://example.com/image.jpg"},
    )
    source: str | None = Field(
        default=None,
        description="Image source e.g. user/upload/provider",
        json_schema_extra={"example": "user"},
    )
    is_thumbnail: bool | None = Field(
        default=None,
        description="Whether this is the thumbnail image",
        json_schema_extra={"example": False},
    )
    metadata: dict | None = Field(
        default=None,
        description="Additional metadata (dimensions, labels, etc.)",
        json_schema_extra={"example": {"width": 800, "height": 600}},
    )


class MealImageCreate(MealImageBase):
    """
    MealImageCreate maps to POST body for new meal image.
    """

    meal_id: int = Field(
        default=...,
        description="Associated meal ID",
        json_schema_extra={"example": 1},
    )
    image_url: str = Field(
        default=...,
        description="Image URL",
        json_schema_extra={"example": "https://example.com/image.jpg"},
    )
    is_thumbnail: bool = Field(
        default=False,
        description="Whether this is the thumbnail image",
        json_schema_extra={"example": False},
    )
    metadata: dict | None = Field(
        default=None,
        description="Additional metadata (dimensions, labels, etc.)",
        json_schema_extra={"example": {"width": 800, "height": 600}},
    )


class MealImageUpdate(MealImageBase):
    """
    MealImageUpdate allows updating image metadata.
    """

    meal_id: int = Field(
        default=...,
        description="Current associated meal ID",
        json_schema_extra={"example": 1},
    )
    photo_id: int = Field(
        default=...,
        description="ID of photo to update",
        json_schema_extra={"example": 2},
    )
    new_meal_id: int | None= Field(
        default=None,
        description="New meal ID to associate with photo (replaces previous meal id)",
        json_schema_extra={"example": 3},
    )


class MealImageRead(BaseModel):
    """
    MealImageRead provides response fields for meal images.
    """

    meal_id: int = Field(default=..., description="Associated meal ID")
    image_url: str = Field(default=..., description="Image URL")
    source: str | None = Field(default=None, description="Image source")
    is_thumbnail: bool = Field(default=False, description="Is thumbnail flag")
    # TODO do we want to send metadata with get requests?
    metadata: dict | None = Field(default=None, description="Image metadata")

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "MealImageRead",
            "examples": [
                {
                    "meal_id": 1,
                    "image_url": "https://example.com/image.jpg",
                    "source": "user",
                    "is_thumbnail": False,
                    "metadata": {"width": 800, "height": 600},
                }
            ],
        },
    )


# ---------- FOODS SCHEMAS ----------

class FoodBase(BaseModel):
    """
    FoodBase class inherits from pydantic BaseModel and provides optional
    fields for request body related to meal api.
    """

    name: str | None = Field(
        default=None,
        description="Food name",
        json_schema_extra={"example": "Grilled Chicken Breast"},
    )
    serving_size_grams: int | None = Field(
        default=None,
        ge=0,
        description="Serving size in grams",
        json_schema_extra={"example": 140},
    )
    calories_per_100_grams: int | None = Field(
        default=None,
        ge=0,
        le=1000,
        description="Calories per 100g",
        json_schema_extra={"example": 165},
    )
    carbs_per_100_grams: int | None = Field(
        default=None,
        ge=0,
        le=1000,
        description="Carbs per 100g",
        json_schema_extra={"example": 0},
    )
    fat_per_100_grams: int | None = Field(
        default=None,
        ge=0,
        le=1000,
        description="Fat per 100g",
        json_schema_extra={"example": 3},
    )
    protein_per_100_grams: int | None = Field(
        default=None,
        ge=0,
        le=1000,
        description="Protein per 100g",
        json_schema_extra={"example": 31},
    )
    micronutrients: dict | None = Field(
        default=None,
        description="Micronutrient breakdown",
        json_schema_extra={"example": {"sodium_mg": 74}},
    )
    ingredients: list[str] | None = Field(
        default=None,
        description="List of ingredients",
        json_schema_extra={"example": ["chicken", "salt", "pepper"]},
    )

# TODO do we need a density field?
class FoodCreate(FoodBase):
    """
    FoodCreate class inherits from FoodBase and maps to fields in POST request
    body for creation of new meal entry.
    """

    name: str = Field(
        default=...,
        description="Food name",
        json_schema_extra={"example": "Grilled Chicken Breast"},
    )
    serving_size_grams: int = Field(
        default=...,
        ge=0,
        description="Serving size in grams",
        json_schema_extra={"example": 140},
    )
    calories_per_100_grams: int = Field(
        default=...,
        ge=0,
        le=1000,
        description="Calories per 100g",
        json_schema_extra={"example": 165},
    )
    carbs_per_100_grams: int = Field(
        default=...,
        ge=0,
        le=1000,
        description="Carbs per 100g",
        json_schema_extra={"example": 0},
    )
    fat_per_100_grams: int = Field(
        default=...,
        ge=0,
        le=1000,
        description="Fat per 100g",
        json_schema_extra={"example": 3},
    )
    protein_per_100_grams: int = Field(
        default=...,
        ge=0,
        le=1000,
        description="Protein per 100g",
        json_schema_extra={"example": 31},
    )


class FoodUpdate(FoodBase):
    """
    FoodUpdate class inherits from FoodBase all optional fields and requires
    meal id  to be provided.
    """

    id: int = Field(
        default=...,
        description="Food ID to update",
        json_schema_extra={"example": 5},
    )


class FoodRead(BaseModel):
    """
    FoodRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """

    id: int = Field(default=..., description="Food ID")
    name: str = Field(default=..., description="Food name")
    serving_size_grams: int = Field(default=..., description="Serving size in grams")
    calories_per_100_grams: int = Field(default=..., description="Calories per 100g")
    carbs_per_100_grams: int = Field(default=..., description="Carbs per 100g")
    fat_per_100_grams: int = Field(default=..., description="Fat per 100g")
    protein_per_100_grams: int = Field(default=..., description="Protein per 100g")
    micronutrients: dict | None = Field(default=None, description="Micros map")
    ingredients: list[str] | None = Field(default=None, description="Ingredients list")

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "FoodRead",
            "examples": [
                {
                    "id": 5,
                    "name": "Grilled Chicken Breast",
                    "serving_size_grams": 140,
                    "calories_per_100_grams": 165,
                    "carbs_per_100_grams": 0,
                    "fat_per_100_grams": 3,
                    "protein_per_100_grams": 31,
                    "micronutrients": {"sodium_mg": 74},
                    "ingredients": ["chicken", "salt", "pepper"],
                }
            ],
        },
    )

# TODO: decide if any schemas are needed for meal-food associations
