from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


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


class MeasurementBase(BaseModel):
    """
    Measurement class inherits from pydantic BaseModel and maps to optional
    fields request body for measurements of blood glucose, blood pressure, etc.
    """

    # TODO: add limits
    measurement_type: Optional[MeasurementType] = Field(
        None,
        description="Type of measurement: bp, hr, ht, wt, or bs. No default.",
        example="bs"
        )
    value_1: Optional[float] = Field(
        None,
        description="value of measurement as float.",
        example=110
        )
    value_2: Optional[float] = Field(
        None,
        description="second value of measurement for blood pressure.",
        example=68
        )
    source: Optional[str] = Field(
        None,
        description="device used to take measurement.",
        example="accucheck"
        )
    time_taken: Optional[datetime] = Field(
        None,
        description="UTC timecode of time measurement was taken.",
        example="2025-11-05T14:30:00Z"
        )
    note: Optional[str] = Field(
        None,
        description="User entered note about measurement"
        )
    symptoms: Optional[str] = Field(
        None,
        description="list of syptoms expereinced at time of measurement",
        example="nausea, clammy"
        )


class MeasurementCreate(MeasurementBase):
    """
    MeasurementCreate class inherits from pydantic MeasurementBase and maps to
    fields in POST request body for measurements of blood glucose, blood
    pressure, etc.
    """

    # TODO: add limits
    measurement_type: MeasurementType = Field(
        ...,
        description="Type of measurement: bp, hr, ht, wt, or bs. No default.",
        example="bs"
        )
    value_1: float = Field(
        ...,
        description="value of measurement as float. No default.",
        example=110
        )
    value_2: Optional[float] = Field(
        None,
        description="""
        second value of measurement for blood pressure. No Default
        """,
        example=68
        )
    source: str = Field(
        "manual",
        description="device used to take measurement. Default is `manual`",
        example="accucheck"
        )
    time_taken: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="""
        UTC timecode of time measurement was taken. Default is `now`
        """,
        example="2025-11-05T14:30:00Z"
        )
    note: Optional[str] = Field(
        None,
        description="User entered note about measurement"
        )
    symptoms: Optional[str] = Field(
        None,
        description="list of syptoms expereinced at time of measurement",
        example="nausea, clammy"
        )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="time entry created"
        )

    @field_validator("value_2")
    @classmethod
    def validate_value2_for_bp(cls, value: float, info):
        mt = info.data.get("measurement_type")
        if mt == MeasurementType.BLOOD_PRESSURE and value is None:
            raise ValueError(
                "value_2 is required for blood pressure measurement"
                )
        elif value is not None:
            raise ValueError(
                "value_2 is only allowed for blood pressure measurement"
            )


class MeasurementUpdate(MeasurementBase):
    """
    MeasurmentUpdate class inherits optional fields from MeasurementBase class
    and implements API owned updated_at timestamp creation.
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="time entry updated"
        )


class MeasurementRead(BaseModel):
    id: int = Field(
        ...,
        description="Database primary key"
        )
    measurement_type: MeasurementType = Field(
        ...,
        description="Type of measurement"
        )
    value_1: float = Field(
        ...,
        description="First value of measurement"
        )
    value_2: Optional[float] = Field(
        None,
        description="Second value of measurement"
        )
    source: str = Field(
        ...,
        description="Source of measurement"
        )
    note: Optional[str] = Field(
        None,
        description="User entered note"
        )
    symptoms: Optional[str] = Field(
        None,
        description="User assessed symptoms at time of measurment"
        )
    time_taken: datetime = Field(
        ...,
        description="Time measurement taken"
        )
    created_at: datetime = Field(
        ...,
        description="Time measurement entry created"
        )
    updated_at: Optional[datetime] = Field(
        None,
        description="Time measurement entry updated"
        )

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
