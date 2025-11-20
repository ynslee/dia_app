"""Base class and functions for defingin database related functions."""


from abc import abstractmethod
import datetime
from typing import List
from pydantic import BaseModel
from schemas.measurement import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementType
)


class Datastore(BaseModel):
    """
    Datastore is the abstract base class for the database and defines the
    methods required.
    """

    @abstractmethod
    async def get_measurement_by_id(self, measurement_id: int):
        """
        abstract method for getting single measuement by id.
        """

    @abstractmethod
    async def create_measurement(self, measuremnt: MeasurementCreate):
        """
        abstract method for creating single measuement.
        """

    @abstractmethod
    async def update_measurement(self, measurement: MeasurementUpdate):
        """
        abstract method for updating single measuement by id.
        """

    @abstractmethod
    async def delete_measurement(self, measurement_id: int):
        """
        abstract method for deleting single measuement by id.
        """

    @abstractmethod
    async def get_all_measuremnts_for_day(self, date: datetime):
        """
        abstract method for getting measuements by date.
        """

    @abstractmethod
    async def bulk_entry_of_measuremnts(
        self,
        measurementes: List[MeasurementCreate]
    ):
        """
        abstract method for creating many measuements.
        """

    @abstractmethod
    async def bulk_update_of_measuremnts(self,
                                         updates: List[MeasurementUpdate]):
        """
        abstract method for updating many measuements.
        """

    @abstractmethod
    async def delete_all_measuremnts_of_a_type(self, m_type: MeasurementType):
        """
        abstract method for deleting many measuements by type.
        """
