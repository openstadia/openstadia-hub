import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from openstadia_hub import schemas
from openstadia_hub.models import User, Server


def get_servers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Server).offset(skip).limit(limit).all()


def has_server_access(db: Session, user_id: int, server_id: int):
    stmt = select(User).join(Server).where(User.id == user_id).where(Server.id == server_id)
    return db.scalars(stmt).one_or_none() is not None


def get_server_by_token(db: Session, token: str):
    return db.query(Server).filter(Server.token == token).first()


def get_server_by_id(db: Session, server_id: int) -> Optional[Server]:
    return db.query(Server).filter(Server.id == server_id).first()


def create_user_server(db: Session, server: schemas.ServerCreate, user_id: int):
    token = secrets.token_urlsafe(16)
    db_item = Server(**server.model_dump(), token=token, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
