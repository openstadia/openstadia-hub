import secrets
from typing import Optional

from sqlalchemy.orm import Session

from openstadia_hub import models, schemas


def get_servers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Server).offset(skip).limit(limit).all()


def get_server_by_token(db: Session, token: str):
    return db.query(models.Server).filter(models.Server.token == token).first()


def get_server_by_id(db: Session, server_id: int) -> Optional[models.Server]:
    return db.query(models.Server).filter(models.Server.id == server_id).first()


def create_user_server(db: Session, server: schemas.ServerCreate, user_id: int):
    token = secrets.token_urlsafe(16)
    db_item = models.Server(**server.model_dump(), token=token, owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
