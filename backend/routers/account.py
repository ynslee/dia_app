from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
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
async def list_users(db: AsyncSession = Depends(get_db)):
	"""
    list_users uses GET and returns all users in the system.
	"""
	result = await db.execute(select(User))
	users = result.scalars().all()
	return users

@router.get(
	path="/users/{user_id}",
	response_model=UserOut,
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    get_user uses GET and returns one user by user_id.
    """
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get(
	path="/me/{user_id}",
	response_model=AccountView,
)
async def get_account_view(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result_profile = await db.execute(
        select(Profile).where(Profile.user_id == user.id)
    )
    profile = result_profile.scalars().first()

    result_settings = await db.execute(
        select(AccountSettings).where(AccountSettings.user_id == user.id)
    )
    settings = result_settings.scalars().first()

    return AccountView(user=user, profile=profile, settings=settings)