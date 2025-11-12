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
        self._measurements = [
            MeasurementCreate(
                measurement_type="bs",
                value_1=97,
                value_2=None,
                time_taken="2025-11-05T14:29:00Z",
                source="accucheck",
                note=None,
                symptoms=None,
                )
            ]
        self._accounts = []

    async def get_measurement_by_id(
        self,
        measurement_id: int,
    ) -> MeasurementRead:
        measurment = MeasurementRead(
            id=measurement_id,
            measurement_type=MeasurementType.BLOOD_PRESSURE,
            value_1=120.0,
            value_2=78.0,
            source="wrist",
            note=None,
            symptoms="lightheaded",
            time_taken=datetime(2025, 11, 5, 14, 29, tzinfo=timezone.utc),
            created_at=datetime(2025, 11, 5, 14, 30, tzinfo=timezone.utc),
            updated_at=None,
            )
        return measurment

    async def create_measurement(self, measuremnt: MeasurementCreate):
        pass

    async def update_measurement(self, measurement: MeasurementUpdate):
        pass

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
