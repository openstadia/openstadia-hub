from enum import Enum
from typing import Optional

from sqlalchemy.orm import Session

from openstadia_hub.crud.server import get_server_by_id
from openstadia_hub.crud.server_access import get_server_access
from openstadia_hub.schemas.user_server_role import UserServerRole


class ServerPermission(Enum):
    CONNECT = 1
    READ_SETTINGS = 2
    WRITE_SETTINGS = 3


def has_server_permission(db: Session, user_id: int, server_id: int, permission: ServerPermission) -> bool:
    server_role = get_server_role(db, user_id, server_id)
    if server_role is None:
        return False

    if permission == ServerPermission.CONNECT:
        return True
    elif permission == ServerPermission.READ_SETTINGS:
        return server_role == UserServerRole.OWNER
    elif permission == ServerPermission.WRITE_SETTINGS:
        return server_role == UserServerRole.OWNER

    return False


def get_server_role(db: Session, user_id: int, server_id: int) -> Optional[UserServerRole]:
    server = get_server_by_id(db, server_id)
    if server.owner_id == user_id:
        return UserServerRole.OWNER

    server_access = get_server_access(db, user_id, server_id)
    if server_access is not None:
        return server_access.role

    return None
