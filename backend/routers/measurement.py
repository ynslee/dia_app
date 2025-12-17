"""Router for handling single measurement API endpoints."""


from database.base import Datastore
from database.mockdb import open_db_sesssion
from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from schemas.measurement import (
    MeasurementCreate,
    MeasurementRead,
    MeasurementUpdate
    )


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"]
)


@router.get(
    path="/{item_id}",
    response_model=MeasurementRead
    )
async def get_mesurement(
    item_id: int,
    db: Datastore = Depends(open_db_sesssion)
    ) -> Response:
    """
    get_measurement uses GET method and returns mesurement with id given as a
    path parameter.
    """
    if item_id < 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "invalid id sent"},
            )
    measurement = await db.get_measurement_by_id(item_id)
    return measurement


# TODO:  do we want it to return the created resposne?
@router.post(
    path="/"
    )
async def create_mesurement(
    mesurement: MeasurementCreate,
    db: Datastore = Depends(open_db_sesssion)
    ) -> Response:
    """
    create_measurement uses POST method.
    """
    new_id = await db.create_measurement(mesurement)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message":"new measurement created", "id":f"{new_id}"}
        )

# TODO: decide if we should return the updated measurment here
@router.patch(
    path="/{item_id}"
    )
async def update_mesurement(
    item_id: int,
    item: MeasurementUpdate,
    db: Datastore = Depends(open_db_sesssion)
    ) -> Response:
    """
    update_measurement uses PATCH method.
    """
    if item_id < 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "invalid id sent"},
            )
    updated = await db.update_measurement(item_id, item)
    # TODO check status code for return
    return updated


@router.delete(
    path="/{item_id}"
    )
async def delete_mesurement(
    item_id: int,
    db: Datastore = Depends(open_db_sesssion)
    ):
    """
    delete_measurement uses DELETE method.
    """
    if item_id < 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "invalid id sent"},
            )
    await db.delete_measurement(item_id)
