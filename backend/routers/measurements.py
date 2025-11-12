from fastapi import APIRouter


"""Router for handling multi-measurement API endpoints."""


router = APIRouter(
    prefix="/measurements",
    tags=["measurements"]
)


@router.get(
    path="/"
    )
def get_measurements():
    """
    get_measurements uses GET method.
    """
    return "I'm a lot of measurements!"


@router.post(
    path="/"
    )
def new_measurements():
    """
    new_measurements uses POST method.
    """
    return "new measurements created"


@router.patch(
    path="/"
    )
def update_measurements():
    """
    update_measurements uses PATCH method.
    """
    return "measurements updated"


@router.delete(
    path="/"
    )
def delete_measurements():
    """
    delete_measurements uses DELETE method.
    """
    return "measurements deleted"
