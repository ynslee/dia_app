from sqlalchemy import select
from db import SessionLocal
from models.account import User
from models.measurements import Measurement, MeasurementType

def main() -> None:
    db = SessionLocal()
    try:
        # build a SELECT * FROM users query
        stmt = select(User)
        result = db.scalars(stmt).all()

        print("Users in DB:")
        for u in result:
            print(f"- id={u.id}, email={u.email}, username={u.username}, is_active={u.is_active}")
        
            """Print all measurements in the database."""
    # order by user_id then time_taken so it's easier to read
        stmt = select(Measurement).order_by(Measurement.user_id, Measurement.time_taken)
        measurements = db.scalars(stmt).all()

        print("\nMeasurements in DB:")
        if not measurements:
            print("  (no measurements found)")
            return

        for m in measurements:
            mt = m.measurement_type.value  # e.g. "bs", "bp"
            print(
                f"  - id={m.id}, user_id={m.user_id}, type={mt}, "
                f"value_1={m.value_1}, value_2={m.value_2}, "
                f"source={m.source}, time_taken={m.time_taken}, "
                f"note={m.note}, symptoms={m.symptoms}"
            )
    finally:
        db.close()

#running it as a script now
if __name__ == "__main__":
    main()
