"""Router for handling single measurement API endpoints."""


from database.base import Datastore
#from database.mockdb import open_db_sesssion
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.measurement import MeasurementRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"]
)


@router.get(
    path="/{item_id}",
    response_model=MeasurementRead
    )
async def get_measurement(item_id: int,
                         db: AsyncSession = Depends(get_db)):
    """
    get_measurement uses GET method and returns mesurement with id given as a
    path parameter.
    """
    measurement = await db.get(measurement, item_id)
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found",
        )
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
