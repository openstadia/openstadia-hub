from datetime import datetime, timezone

from sqlalchemy.orm import Session

from openstadia_hub.crud.server_access import get_server_access
from openstadia_hub.models.server_invite import ServerInvite as DbServerInvite
from openstadia_hub.services.server_permission import has_server_permission, ServerPermission


def can_activate_server_invite(db: Session, server_invite: DbServerInvite) -> bool:
    server_id = server_invite.server_id

    if server_invite.activated:
        return False

    if server_invite.expiration_date < datetime.now(timezone.utc):
        return False

    if not has_server_permission(db, server_invite.created_by, server_id, ServerPermission.WRITE_SETTINGS):
        return False

    return True


def can_activate_server_invite_by_user(db: Session, server_invite: DbServerInvite, user_id: int) -> bool:
    server_id = server_invite.server_id

    if not can_activate_server_invite(db, server_invite):
        return False

    server_access = get_server_access(db=db, user_id=user_id, server_id=server_id)
    if server_access is not None:
        return False

    return True
