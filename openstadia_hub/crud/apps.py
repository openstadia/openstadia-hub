from sqlalchemy import select
from sqlalchemy.orm import Session

from openstadia_hub.models import User, Server, App


def get_apps(db: Session, user_id: int):
    stmt = select(App).join(Server).join(User).where(User.id == user_id)
    return db.scalars(stmt).all()
