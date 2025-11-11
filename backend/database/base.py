from abc import abstractmethod
import datetime
from typing import List
from pydantic import BaseModel
from models.measurement import MeasurementCreate, MeasurementUpdate
from models.measurement import MeasurementType


class Datastore(BaseModel):
    """
    Datastore is the abstract base class for the database and defines the
    methods required.
    """

    @abstractmethod
    async def get_measurement_by_id(self, id: int):
        pass

    @abstractmethod
    async def create_measurement(self, measuremnt: MeasurementCreate):
        pass

    @abstractmethod
    async def update_measurement(self, measurement: MeasurementUpdate):
        pass

    @abstractmethod
    async def delete_measurement(self, id: int):
        pass

    @abstractmethod
    async def get_all_measuremnts_for_day(self, date: datetime):
        pass

    @abstractmethod
    async def bulk_entry_of_measuremnts(
        self,
        measurementes: List[MeasurementCreate]
    ):
        pass

    @abstractmethod
    async def bulk_update_of_measuremnts(self,
                                         updates: List[MeasurementUpdate]):
        pass

    @abstractmethod
    async def delete_all_measuremnts_of_a_type(self, type: MeasurementType):
        pass
