from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field, Optional


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


class MeasurementCreate(BaseModel):
    """
    Measurement class inherits from pydantic BaseModel and maps to fields in
    POST request body for measurements of blood glucose, blood pressure, etc.
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
        description="second value of measurement for blood pressure. No Default",
        example=68
        )
    source: str = Field(
        "manual",
        description="device used to take measurement. Default is `manual`",
        example="accucheck"
        )
    time_taken: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timecode of time measurement was taken. Default is time recieved (`now`)",
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
    created: datetime = Field(
		default_factory=lambda: datetime.now(timezone.utc),
        description="time entry created"
	)
