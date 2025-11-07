from abc import abstractmethod
import datetime
from typing import List
from pydantic import BaseModel
from backend.models.measurement import MeasurementCreate, MeasurementUpdate
from backend.models.measurement import MeasurementType


class Datastore(BaseModel):
    """
    Datastore is the abstract base class for the database and defines the
    methods required.
    """

    @abstractmethod
    async def get_measurement_by_id(id: int):
        pass

    @abstractmethod
    async def create_measurement(measuremnt: MeasurementCreate):
        pass

    @abstractmethod
    async def update_measurement(measurement: MeasurementUpdate):
        pass

    @abstractmethod
    async def delete_measurement(id: int):
        pass

    @abstractmethod
    async def get_all_measuremnts_for_day(date: datetime):
        pass

    @abstractmethod
    async def bulk_entry_of_measuremnts(
        measurementes: List[MeasurementCreate]
    ):
        pass

    @abstractmethod
    async def bulk_update_of_measuremnts(updates: List[MeasurementUpdate]):
        pass

    @abstractmethod
    async def delete_all_measuremnts_of_a_type(type: MeasurementType):
        pass
