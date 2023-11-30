import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from openstadia_hub.models.server_invite import ServerInvite


def get_server_invite_by_id(db: Session, invite_id: int) -> Optional[ServerInvite]:
    stmt = select(ServerInvite).where(ServerInvite.id == invite_id)
    return db.scalars(stmt).one_or_none()


def get_server_invites(db: Session, server_id: int) -> List[ServerInvite]:
    stmt = select(ServerInvite).where(ServerInvite.server_id == server_id)
    return list(db.scalars(stmt).all())


def disable_server_invite(db: Session, server_invite: ServerInvite) -> Optional[ServerInvite]:
    server_invite.activated = True
    db.commit()

    return server_invite


def create_server_invite(db: Session, user_id: int, server_id: int) -> ServerInvite:
    token = secrets.token_urlsafe(32)
    created_at = datetime.now(timezone.utc)
    expiration_date = created_at + timedelta(days=1)

    server_invite = ServerInvite(
        token=token,
        activated=False,
        created_at=created_at,
        expiration_date=expiration_date,
        created_by=user_id,
        server_id=server_id
    )

    db.add(server_invite)
    db.commit()
    db.refresh(server_invite)
    return server_invite


def get_server_invite_by_token(db: Session, token: str) -> Optional[ServerInvite]:
    stmt = select(ServerInvite).where(ServerInvite.token == token)
    return db.scalars(stmt).one_or_none()


def activate_server_invite(db: Session, server_invite: ServerInvite, user_id: int) -> Optional[ServerInvite]:
    server_invite.activated = True
    server_invite.activated_by = user_id
    server_invite.activated_at = datetime.now(timezone.utc)
    db.commit()

    return server_invite
