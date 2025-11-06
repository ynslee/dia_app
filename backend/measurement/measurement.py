from fastapi import APIRouter


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"]
)


@router.get(
    path="/{item_id}"
    )
def get_mesurement(item_id: int):
    return "I'm a mesurement!"


@router.post(
    path="/"
    )
def create_mesurement():
    return "new user measurement"


@router.patch(
    path="/{item_id}"
    )
def update_mesurement(item_id: int):
    return "new user measurement"


@router.delete(
    path="/{item_id}"
    )
def delete_mesurement(item_id: int):
    return "new user measurement"
