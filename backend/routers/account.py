from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import get_db
from models.account import User, Profile, AccountSettings
from schemas.account import UserOut, AccountView

#TODO: async in measurement router
router = APIRouter(
	prefix="/account",
	tags=["account"])

@router.get(
	path="/users",
	response_model=list[UserOut],
)
def list_users(db: Session = Depends(get_db)):
	"""
    list_users uses GET and returns all users in the system.
	"""
	users = db.scalars(select(User)).all()
	return users

@router.get(
	path="/users/{user_id}",
	response_model=UserOut,
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    get_user uses GET and returns one user by user_id.
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get(
	path="/me/{user_id}",
	response_model=AccountView,
)
def get_account_view(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.scalar(select(Profile).where(Profile.user_id == user.id))
    settings = db.scalar(
        select(AccountSettings).where(AccountSettings.user_id == user.id)
    )

    return AccountView(user=user, profile=profile, settings=settings)