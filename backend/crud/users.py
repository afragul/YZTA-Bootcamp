from sqlalchemy.orm import Session

from auth import hash_password
from models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, password: str) -> User:
    user = User(email=email.lower().strip(), hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
