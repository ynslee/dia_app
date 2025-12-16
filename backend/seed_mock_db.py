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
from models.measurements import Measurement, MeasurementType
from datetime import datetime, timezone

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

def seed_measurements() -> None:
    db = SessionLocal()
    try:
        # Clear existing measurements if you want a clean slate:
        # db.query(Measurement).delete()
        # db.commit()

        examples = [
            # --- User 1 ---
            Measurement(
                measurement_type=MeasurementType.BLOOD_SUGAR,
                value_1=6.1,
                value_2=None,
                source="manual",
                time_taken=datetime(2025, 11, 5, 7, 30, tzinfo=timezone.utc),
                note="Fasting before breakfast",
                symptoms=None,
                user_id=1,
            ),
            Measurement(
                measurement_type=MeasurementType.BLOOD_SUGAR,
                value_1=8.5,
                value_2=None,
                source="manual",
                time_taken=datetime(2025, 11, 5, 9, 0, tzinfo=timezone.utc),
                note="2h after oatmeal",
                symptoms="a bit tired",
                user_id=1,
            ),
            Measurement(
                measurement_type=MeasurementType.BLOOD_PRESSURE,
                value_1=120,
                value_2=78,  # diastolic -> must NOT be None for bp
                source="omron cuff",
                time_taken=datetime(2025, 11, 5, 9, 5, tzinfo=timezone.utc),
                note="Sitting, left arm",
                symptoms="lightheaded",
                user_id=1,
            ),
            Measurement(
                measurement_type=MeasurementType.HEART_RATE,
                value_1=72,
                value_2=None,
                source="fitbit",
                time_taken=datetime(2025, 11, 5, 9, 5, tzinfo=timezone.utc),
                note="Resting 5 min",
                symptoms=None,
                user_id=1,
            ),
            Measurement(
                measurement_type=MeasurementType.WEIGHT,
                value_1=68.5,
                value_2=None,
                source="smart scale",
                time_taken=datetime(2025, 11, 5, 7, 25, tzinfo=timezone.utc),
                note=None,
                symptoms=None,
                user_id=1,
            ),
            Measurement(
                measurement_type=MeasurementType.HEIGHT,
                value_1=165.0,
                value_2=None,
                source="clinic",
                time_taken=datetime(2025, 1, 10, 10, 0, tzinfo=timezone.utc),
                note="Measured at clinic",
                symptoms=None,
                user_id=1,
            ),

            # --- User 2 ---
            Measurement(
                measurement_type=MeasurementType.BLOOD_SUGAR,
                value_1=7.8,
                value_2=None,
                source="manual",
                time_taken=datetime(2025, 11, 5, 7, 15, tzinfo=timezone.utc),
                note="Fasting",
                symptoms=None,
                user_id=2,
            ),
            Measurement(
                measurement_type=MeasurementType.BLOOD_SUGAR,
                value_1=10.2,
                value_2=None,
                source="manual",
                time_taken=datetime(2025, 11, 5, 21, 30, tzinfo=timezone.utc),
                note="2h after pasta",
                symptoms="nausea",
                user_id=2,
            ),
            Measurement(
                measurement_type=MeasurementType.BLOOD_PRESSURE,
                value_1=140,
                value_2=90,
                source="home cuff",
                time_taken=datetime(2025, 11, 5, 21, 35, tzinfo=timezone.utc),
                note="After dinner",
                symptoms="headache",
                user_id=2,
            ),
            Measurement(
                measurement_type=MeasurementType.WEIGHT,
                value_1=83.0,
                value_2=None,
                source="bathroom scale",
                time_taken=datetime(2025, 11, 4, 7, 20, tzinfo=timezone.utc),
                note=None,
                symptoms=None,
                user_id=2,
            ),
            Measurement(
                measurement_type=MeasurementType.HEART_RATE,
                value_1=95,
                value_2=None,
                source="fitbit",
                time_taken=datetime(2025, 11, 4, 18, 0, tzinfo=timezone.utc),
                note="30 min walk",
                symptoms=None,
                user_id=2,
            ),
        ]

        db.add_all(examples)
        db.commit()
        print(f"Inserted {len(examples)} mock measurements.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_mock_data()
    seed_measurements()
