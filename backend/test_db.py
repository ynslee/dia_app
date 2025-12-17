from sqlalchemy import select
from db import SessionLocal
from models.account import User
from models.measurements import Measurement
import asyncio

async def main() -> None:
    # open an async DB session
    async with SessionLocal() as db:
        # ---- Users ----
        result = await db.execute(select(User))
        users = result.scalars().all()

        print("Users in DB:")
        if not users:
            print("  (no users found)")
        for u in users:
            print(
                f"- id={u.id}, email={u.email}, "
                f"username={u.username}, is_active={u.is_active}"
            )

        # ---- Measurements ----
        # order by user_id then time_taken so it's easier to read
        result_meas = await db.execute(
            select(Measurement).order_by(Measurement.user_id, Measurement.time_taken)
        )
        measurements = result_meas.scalars().all()

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

#running it as a script now
if __name__ == "__main__":
    asyncio.run(main())
