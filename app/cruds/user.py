from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hashed
from app.schemas.user import CreateUser


def get_user_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def create_user(db: Session, user: CreateUser):
    hashed_password = get_password_hashed(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
