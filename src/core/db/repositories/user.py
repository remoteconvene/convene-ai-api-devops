import hashlib

from sqlalchemy.orm import Session

from src.core.db.models.user import User
from src.core.db.sql_session_manager import get_db


def add_default_user():
    with get_db() as db:
        if not user_exists(db, "admin", "admin@azeus.com"):
            password = "p@ssw0rd1234"
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            new_user = User(
                first_name="Super",
                last_name="Admin",
                email="admin@azeus.com",
                username="admin",
                hashed_password=hashed_password,
                superuser=True,
                status=True,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print("User created successfully")
            return new_user
        else:
            print("User already exists")
            return True


def user_exists(db: Session, username: str, email: str) -> bool:
    return (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
        is not None
    )


def get_user(username: str):
    with get_db() as db:
        user: User = db.query(User).filter(User.username == username).one_or_none()
        return user


def update_user_token(username: str, token: str):
    with get_db() as db:
        db.query(User).filter(User.username == username).update({"jwt_token": token})
        db.commit()
