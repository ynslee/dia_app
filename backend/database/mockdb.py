"""Mock database class and functions."""


from datetime import datetime, timezone
from typing import List
from database.base import Datastore
from models.measurement import (
    MeasurementCreate,
    MeasurementUpdate,
    MeasurementType,
    MeasurementRead
)


class MockDB(Datastore):
    """
    MockDB inherits from Datastore and provides a mock database object with
    dummy data and implements all abstract methods from Datastore methods.
    """

    def __init__(self):
        super().__init__()
        self._next_id = 2
        self._measurements = {
            1: {
                "measurement_type": "bp",
                "value_1": 120,
                "value_2": 78,
                "time_taken": datetime.now(timezone.utc),
                "source":"wrist",
                "note": None,
                "symptoms": "lightheaded",
                "updated_at": datetime.now(timezone.utc),
                "created_at": datetime.now(timezone.utc),
                },
        }
        self._accounts = []

    async def get_measurement_by_id(
        self,
        measurement_id: int,
    ) -> MeasurementRead:
        measurement = self._measurements[measurement_id]
        return MeasurementRead(id=measurement_id, **measurement)

    async def create_measurement(self, measurement: MeasurementCreate):
        
        now = datetime.now(timezone.utc)

        data = measurement.model_dump()
        data["created_at"] = now
        data["updated_at"] = now

        new_id = self._next_id
        self._next_id += 1

        self._measurements[new_id] = data
        return new_id
        # return MeasurementRead(id=new_id, **data)

    async def update_measurement(
        self,
        measurement_id:int,
        measurement: MeasurementUpdate
        ):
        
        existing = self._measurements[measurement_id]
        update_data = measurement.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            existing[key] = value

        existing["updated_at"] = datetime.now(timezone.utc)
        self._measurements[measurement_id] = existing

        return MeasurementRead(id=measurement_id, **existing)

    async def delete_measurement(self, measurement_id: int):
        pass

    async def get_all_measuremnts_for_day(self, date: datetime):
        pass

    async def bulk_entry_of_measuremnts(
        self,
        measurementes: List[MeasurementCreate]
    ):
        pass

    async def bulk_update_of_measuremnts(self,
                                         updates: List[MeasurementUpdate]):
        pass

    async def delete_all_measuremnts_of_a_type(self, m_type: MeasurementType):
        pass


def open_db_sesssion():
    """
    open_db_session returns MockDB instance for testing purposes.
    """
    return MockDB()
