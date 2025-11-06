from fastapi import APIRouter


router = APIRouter(
    prefix="/measurements",
    tags=["measurements"]
)


@router.get(
    path="/"
    )
def get_measurements():
    return "I'm a lot of measurements!"


@router.post(
    path="/"
    )
def new_measurements():
    return "new measurements created"


@router.patch(
    path="/"
    )
def update_measurements():
    return "measurements updated"


@router.delete(
    path="/"
    )
def delete_measurements():
    return "measurements deleted"
