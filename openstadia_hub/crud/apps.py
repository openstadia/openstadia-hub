from sqlalchemy import select
from sqlalchemy.orm import Session

from openstadia_hub.models import User, Server, App


def get_apps_by_user_id(db: Session, user_id: int):
    stmt = select(App).join(Server).join(User).where(User.id == user_id)
    return db.scalars(stmt).all()


def get_apps_by_server_id(db: Session, server_id: int):
    stmt = select(App).join(Server).where(Server.id == server_id)
    return db.scalars(stmt).all()
