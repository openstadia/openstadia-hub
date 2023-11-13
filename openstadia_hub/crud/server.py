from typing import Optional, Any, Sequence

from sqlalchemy import select, Row
from sqlalchemy.orm import Session

from openstadia_hub.core.server_token import generate_server_token
from openstadia_hub.models import Server
from openstadia_hub.models.server_access import ServerAccess
from openstadia_hub.schemas.server import ServerCreate
from openstadia_hub.schemas.user_server_role import UserServerRole


def get_server_by_token(db: Session, token: str) -> Optional[Server]:
    stmt = select(Server).where(Server.token == token)
    return db.scalars(stmt).one_or_none()


def get_server_by_id(db: Session, server_id: int) -> Optional[Server]:
    stmt = select(Server).where(Server.id == server_id)
    return db.scalars(stmt).one_or_none()


def create_user_server(db: Session, server_create: ServerCreate, user_id: int):
    token = generate_server_token()
    server = Server(**server_create.model_dump(), token=token, owner_id=user_id)
    db.add(server)
    db.flush()
    db.refresh(server)

    server_access = ServerAccess(server_id=server.id, user_id=user_id, role=UserServerRole.OWNER)
    db.add(server_access)

    db.commit()
    return server


def delete_server_by_id(db: Session, server_id: int) -> Optional[Server]:
    stmt = select(Server).filter_by(id=server_id)
    server = db.scalars(stmt).first()
    db.delete(server)
    db.commit()
    return server


def regenerate_server_token(db: Session, server_id: int) -> Optional[Server]:
    server = get_server_by_id(db, server_id)
    if server is None:
        return None

    server.token = generate_server_token()
    db.commit()
    return server


def get_user_servers(db: Session, user_id: int) -> Sequence[Row[tuple[Any, Any, Any, Any]]]:
    stmt = select(Server.id, Server.name, Server.owner_id, ServerAccess.role).join(ServerAccess).where(
        ServerAccess.user_id == user_id)
    return db.execute(stmt).all()


def get_servers(db: Session) -> Sequence[Server]:
    stmt = select(Server)
    return db.scalars(stmt).all()
