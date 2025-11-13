from enum import Enum
from sqlalchemy import (
    Column,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
    ForeignKeyConstraint
)


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


class Measurement(): #inherit base class
    __measurement__ = "users"