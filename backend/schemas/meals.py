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
		  description="id of meal if already created",
		  json_schema_extra={"example":"3"}
	    )
    carbs: int | None = Field(
      default=None,
		  description="total amount of carbs in meal in grams",
		  json_schema_extra={"example":"120"}
		  )
    protein: int | None = Field(
		  default=None,
		  description="total amount of protein in meal in grams",
		  json_schema_extra={"example":"11"}
		  )
    fat: int | None = Field(
		  default=None,
		  description="total amount of fat in meal in grams",
		  json_schema_extra={"example":"18"}
		  )
    calories: int | None = Field(
		  default=None,
		  description="total calories in meal",
		  json_schema_extra={"example":"450"}
		  )
    time_of_meal: datetime | None = Field(
		  default=None,
		  description="UTC timecode of date and time of meal",
		  json_schema_extra={"example":"2025-12-05T14:30:00Z"}
		  )
    note: str | None = Field(
		  default=None,
		  description="User provided note",
		  json_schema_extra={"example":"my note"}
		  )
    meal_type: MealType | None = Field(
		  default=MealType.UNSPECIFIED,
		  description="Meal Type: Breakfast, Lunch, Dinner, Snack, Unspecified",
		  json_schema_extra={"example":"Lunch"}
		  )
    location: Location | None = Field(
		  default=Location.UNSPECIFIED,
		  description="location of meal: home, restaurent, unspecified",
		  json_schema_extra={"example":"home"}
		  )


# TODO what do we want to require for the meals?
class MealCreate(MealBase):
    """
    MealCreate class inherits from MealBase and maps to fields in POST request
    body for creation of new meal entry.
    """

    carbs: int | None = Field(
      default=None,
		  description="total amount of carbs in meal in grams",
		  json_schema_extra={"example":"120"}
		  )
    protein: int | None = Field(
		  default=None,
		  description="total amount of protein in meal in grams",
		  json_schema_extra={"example":"11"}
		  )
    fat: int | None = Field(
		  default=None,
		  description="total amount of fat in meal in grams",
		  json_schema_extra={"example":"18"}
		  )
    calories: int | None = Field(
		  default=None,
		  description="total calories in meal",
		  json_schema_extra={"example":"450"}
		  )
    time_of_meal: datetime = Field(
		  default_factory=lambda: datetime.now(timezone.utc),
		  description="UTC timecode of date and time of meal",
		  json_schema_extra={"example":"2025-12-05T14:30:00Z"}
		  )
    note: str | None = Field(
		  default=None,
		  description="User provided note",
		  json_schema_extra={"example":"my note"}
		  )
    meal_type: MealType = Field(
		  default=MealType.UNSPECIFIED,
		  description="Meal Type: Breakfast, Lunch, Dinner, Snack, Unspecified",
		  json_schema_extra={"example":"Lunch"}
		  )
    location: Location = Field(
		  default=Location.UNSPECIFIED,
		  description="location of meal: home, restaurent, unspecified",
		  json_schema_extra={"example":"home"}
		  )


class MealUpdate(MealBase):
    """
    MealUpdate class inherits from MealBase all optional fields and requires
    meal id  to be provided.
    """
    
    id: int = Field(
      default=...,
		  description="id of meal to update",
		  json_schema_extra={"example":"3"}
		  )


class MealRead(BaseModel):
    """
    MealRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """
    
    id: int = Field(
      default=...,
		  description="id of meal if already created",
		  )
    carbs: int | None = Field(
		  default=...,
		  description="total amount of carbs in meal in grams",
		  )
    protein: int | None = Field(
		  default=...,
		  description="total amount of protein in meal in grams",
		  )
    fat: int | None = Field(
		  default=...,
		  description="total amount of fat in meal in grams",
		  )
    calories: int | None = Field(
		  default=...,
		  description="total calories in meal",
		  )
    time_of_meal: datetime = Field(
		  default=...,
		  description="UTC timecode of date and time of meal",
		  )
    note: str | None = Field(
		  default=...,
		  description="User provided note",
		  )
    meal_type: MealType = Field(
		  default=...,
		  description="Meal Type: Breakfast, Lunch, Dinner, Snack, Unspecified",
		  )
    location: Location = Field(
		  default=...,
		  description="location of meal: home, restaurent, unspecified",
		  )
    created_at: datetime = Field(
        default=...,
        description="Time measurement entry created"
        )
    updated_at: datetime | None = Field(
        default=None,
        description="Time measurement entry updated"
        )
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "MealRead",
            "examples": [
                {
                    "id": 1,
                    "carbs": 30,
                    "protein": 15,
                    "fat": 16,
                    "calories": 398,
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
    
    schedule: dict | None = Field(
		default=None,
		description="",
		json_schema_extra={"example":""}
	)
    is_active: bool | None = Field(
		default=None,
		description="",
		json_schema_extra={"example":""}
	)
    show_calories: bool | None = Field(
		default=None,
		description="",
		json_schema_extra={"example":""}
	)
    reminder_time_before_min: int | None = Field(
		default=None,
		description="",
		json_schema_extra={"example":""}
	)


class MealSettingsUpdate(MealSettingsBase):
    """
    MealSettingsUpdate class inherits from MealSettingsBase all optional fields.
    """


class MealSettingsRead(BaseModel):
    """
    MealSettingsRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """
    
    schedule: dict | None = Field()
    is_active: bool | None = Field()
    show_calories: bool | None = Field()
    reminder_time_before_min: int | None = Field()


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "title": "MeasurementRead",
            "examples": [
                {
                    "id": 1,
                    "measurement_type": "bp",
                    "value_1": 120,
                    "value_2": 78,
                    "source": "wrist",
                    "note": None,
                    "symptoms": "lightheaded",
                    "time_taken": "2025-11-05T14:29:00Z",
                    "created_at": "2025-11-05T14:30:00Z",
                    "updated_at": None
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
    
    meal_id: int | None = Field()
    image_url: str | None = Field()
    source: str | None = Field()
    is_thumbnail: bool | None = Field()
    metadata: dict | None = Field()


class MealImgaeCreate(MealImageBase):
    """
    MealImgaeCreate class inherits from MealBase and maps to fields in POST
    request body for creation of new meal entry.
    """


class MealImageUpdate(MealImageBase):
    """
    MealImageUpdate class inherits from MealImageBase all optional fields and
    requires meal id  to be provided.
    """


class MealImageRead(BaseModel):
    """
    MealImageRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """


# ---------- FOODS SCHEMAS ----------

class FoodBase(BaseModel):
    """
    FoodBase class inherits from pydantic BaseModel and provides optional
    fields for request body related to meal api.
    """

    name: str | None = Field()
    serving_size_grams: int | None = Field()
    calories_per_100_grams: int | None = Field()
    carbs_per_100_grams: int | None = Field()
    fat_per_100_grams: int | None = Field()
    protein_100_grams: int | None = Field()
    micronutrients: dict | None = Field()
    ingredients: list[str] | None = Field()


class FoodCreate(FoodBase):
    """
    FoodCreate class inherits from FoodBase and maps to fields in POST request
    body for creation of new meal entry.
    """


class FoodUpdate(FoodBase):
    """
    FoodUpdate class inherits from FoodBase all optional fields and requires
    meal id  to be provided.
    """


class FoodRead(BaseModel):
    """
    FoodRead class inherits from pydantic BaseModel and provides all
    fields needed for fufillment of GET requests.
    """
