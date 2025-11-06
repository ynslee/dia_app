from fastapi import APIRouter


router = APIRouter(
    prefix="/measurement",
    tags=["measurement"]
)


@router.get(
    path="/"
    )
def get_mesurement():
    return "I'm a mesurement!"


@router.post(
    path="/"
    )
def new_mesurement():
    return "new user measurement"


@router.patch(
    path="/"
    )
def new_mesurement():
    return "new user measurement"


@router.delete(
    path="/"
    )
def new_mesurement():
    return "new user measurement"
