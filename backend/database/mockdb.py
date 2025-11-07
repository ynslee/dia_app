import datetime
from backend.database.base import Datastore
from typing import List
from backend.models.measurement import MeasurementCreate, MeasurementUpdate
from backend.models.measurement import MeasurementType


class MockDB(Datastore):
    """
    MockDB inherits from Datastore and provides a mock database object with
    dummy data and implements all abstract methods from Datastore methods.
    """
    
    def __init__(self):
        self._measurements = [
            MeasurementCreate(
                measurement_type="bs",
                value_1=97,
                value_2=None,
                time_taken="2025-11-05T14:29:00Z",
                source="accucheck",
                note=None,
                symptoms=None,
                created_at=None,
			)
            ]
        self._accounts = []
    
    async def get_measurement_by_id(id: int):
        pass
    
    
    async def create_measurement(measuremnt: MeasurementCreate):
        pass


    async def update_measurement(measurement: MeasurementUpdate):
        pass


    async def delete_measurement(id: int):
        pass


    async def get_all_measuremnts_for_day(date: datetime):
        pass


    async def bulk_entry_of_measuremnts(
        measurementes: List[MeasurementCreate]
    ):
        pass


    async def bulk_update_of_measuremnts(updates: List[MeasurementUpdate]):
        pass


    async def delete_all_measuremnts_of_a_type(type: MeasurementType):
        pass
