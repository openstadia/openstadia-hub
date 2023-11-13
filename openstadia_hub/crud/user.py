from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from openstadia_hub.models import User
from openstadia_hub.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return db.scalars(stmt).one_or_none()


def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).one_or_none()


def get_user_by_auth_id(db: Session, auth_id: str):
    stmt = select(User).where(User.auth_id == auth_id)
    return db.scalars(stmt).one_or_none()


def get_user_by_uniques(db: Session, username: str, auth_id: str, email: str):
    stmt = select(User).where(
        or_(
            User.email == email,
            User.auth_id == auth_id,
            User.username == username,
        )
    )
    return db.scalars(stmt).first()


def create_user(db: Session, user: UserCreate, auth_id: str, email: str):
    db_user = User(username=user.username, auth_id=auth_id, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
