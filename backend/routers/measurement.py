from fastapi import APIRouter, Depends
from database.base import Datastore
from database.mockdb import open_db_sesssion
from models.measurement import MeasurementRead


"""Router for handling single measurement API endpoints."""


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"]
)


@router.get(
    path="/{item_id}",
    response_model=MeasurementRead
    )
async def get_mesurement(item_id: int,
                         db: Datastore = Depends(open_db_sesssion)):
    """
    get_measurement uses GET method and returns mesurement with id given as a
    path parameter.
    """
    measurement = await db.get_measurement_by_id(item_id)
    return measurement


@router.post(
    path="/"
    )
def create_mesurement():
    """
    create_measurement uses POST method.
    """
    return "new measurement created"


@router.patch(
    path="/{item_id}"
    )
def update_mesurement(item_id: int):
    """
    update_measurement uses PATCH method.
    """
    return "measurement updated"


@router.delete(
    path="/{item_id}"
    )
def delete_mesurement(item_id: int):
    """
    delete_measurement uses DELETE method.
    """
    return "measurement deleted"
