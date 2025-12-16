from db import Base, engine
from models import account, measurements
# noqa: F401  - just to register models


def init_db() -> None:
    print("Removing any existing tables in mock database...")
    Base.metadata.drop_all(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("✅ Mock DB schema ready.")


if __name__ == "__main__":
    init_db()
