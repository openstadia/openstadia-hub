from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from openstadia_hub.models.server_access import ServerAccess
from openstadia_hub.schemas.user_server_role import UserServerRole


def create_server_access(db: Session, user_id: int, server_id: int, role: UserServerRole) -> ServerAccess:
    server_access = ServerAccess(user_id=user_id, server_id=server_id, role=role)
    db.add(server_access)
    db.commit()
    db.refresh(server_access)
    return server_access


def get_server_access(db: Session, user_id: int, server_id: int) -> Optional[ServerAccess]:
    stmt = select(ServerAccess).where(ServerAccess.server_id == server_id).where(ServerAccess.user_id == user_id)
    return db.scalars(stmt).one_or_none()


def delete_server_access(db: Session, user_id: int, server_id: int) -> Optional[ServerAccess]:
    stmt = select(ServerAccess).where(ServerAccess.server_id == server_id).where(ServerAccess.user_id == user_id)
    server_access = db.scalars(stmt).one_or_none()
    db.delete(server_access)
    db.commit()
    return server_access
