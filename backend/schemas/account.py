#if enum values changed in models.py, API will change too(just keep in mind)
from models.account import Gender, DiabetesType, Units, BGUnits
#validate dta for requests and control reponses(basemodel)
from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict
from datetime import datetime

#username optional atm
class UserCreate(BaseModel):
    """Body for creating a user (no auth yet)."""
    email: EmailStr
    username: str | None = Field(default=None, max_length=50)

class UserUpdate(BaseModel):
    """Used to partially update a user (PATCH). All fields optional."""
    email: EmailStr | None = None
    username: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None

class UserOut(BaseModel):
    """What you return to the client when you send user data."""
    id: int
    email: EmailStr
    username: str | None = Field(default=None, max_length=50)
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Tell Pydantic v2 it can build from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)

#Noneedto create profile when building the account. Maybe want to change
#later into building profilecreate+update.
#maybe age and height shouldn't be optional?
class ProfileIn(BaseModel):
    """Profile fields that client can set/update."""
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)
    #age: int | None = Field(default=None, ge=0, le=120)
    age: int | None = Field(ge=0, le=120)
    height_cm: int | None = Field(ge=30, le=260)
    #height_cm: int | None = Field(default=None, ge=30, le=260)

    # Use enums from models
    gender: Gender = Gender.undisclosed
    diabetes_type: DiabetesType = DiabetesType.none


class ProfileOut(ProfileIn):
    """Profile as returned from API."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- SETTINGS SCHEMAS ----------

class SettingsIn(BaseModel):
    """Body for updating settings. All optional for PATCH."""
    dark_mode: bool | None = None
    email_notifications_enabled: bool | None = None
    push_notifications_enabled: bool | None = None
    preferred_units: Units | None = None
    preferred_units_BG: BGUnits | None = None
    checklist: dict | None = None


class SettingsOut(BaseModel):
    """Settings as returned from API."""
    id: int
    dark_mode: bool
    email_notifications_enabled: bool
    push_notifications_enabled: bool
    preferred_units: Units
    preferred_units_BG: BGUnits
    checklist: dict
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- COMBINED VIEW ----------

class AccountView(BaseModel):
    """Nice combined object for /v1/account/me, etc."""
    user: UserOut
    profile: ProfileOut | None = None
    settings: SettingsOut | None = None