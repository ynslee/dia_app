# test_db_connection.py

from sqlalchemy import select
from db import SessionLocal
from models.account import User

def main() -> None:
    db = SessionLocal()
    try:
        # build a SELECT * FROM users query
        stmt = select(User)
        result = db.scalars(stmt).all()

        print("Users in DB:")
        for u in result:
            print(f"- id={u.id}, email={u.email}, username={u.username}, is_active={u.is_active}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
