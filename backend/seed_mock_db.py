# seed_mock_db.py

from db import SessionLocal, Base, engine
from models.account import (
    User,
    Profile,
    AccountSettings,
    Gender,
    DiabetesType,
    Units,
    BGUnits,
)


def seed_mock_data() -> None:
    # Make sure tables exist (safe if already created)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Clear existing rows
        db.query(AccountSettings).delete()
        db.query(Profile).delete()
        db.query(User).delete()
        db.commit()

        # Create User
        user1 = User(
            email="alice@example.com",
            username="alice",
            is_active=True,
        )
        db.add(user1)
        db.flush()  # gets user1.id from DB

        profile1 = Profile(
            user_id=user1.id,
            first_name="Alice",
            last_name="Smith",
            age=32,
            height_cm=165,
            gender=Gender.female,
            diabetes_type=DiabetesType.type1,
        )

        settings1 = AccountSettings(
            user_id=user1.id,
            dark_mode=False,
            email_notifications_enabled=True,
            push_notifications_enabled=True,
            preferred_units=Units.metric,
            preferred_units_BG=BGUnits.mmol,
            checklist={"onboarding_done": True},
        )

        db.add_all([profile1, settings1])

        # 3) Create User 2
        user2 = User(
            email="bob@example.com",
            username="bob",
            is_active=True,
        )
        db.add(user2)
        db.flush()  # gets user2.id

        profile2 = Profile(
            user_id=user2.id,
            first_name="Bob",
            last_name="Lee",
            age=45,
            height_cm=178,
            gender=Gender.male,
            diabetes_type=DiabetesType.type2,
        )

        settings2 = AccountSettings(
            user_id=user2.id,
            dark_mode=True,
            email_notifications_enabled=True,
            push_notifications_enabled=False,
            preferred_units=Units.imperial,
            preferred_units_BG=BGUnits.mg,
            checklist={"onboarding_done": False},
        )

        db.add_all([profile2, settings2])

        # 4) Save everything
        db.commit()
        print("✅ Seeded mock users, profiles and settings.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_mock_data()
