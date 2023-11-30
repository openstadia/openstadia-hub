from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.server_access import create_server_access
from openstadia_hub.crud.server_invites import (
    create_server_invite, get_server_invite_by_token, activate_server_invite, get_server_invites,
    get_server_invite_by_id, disable_server_invite)
from openstadia_hub.schemas.server_invite import (
    ServerInvite, ServerInviteInfo, ServerInviteToken, ServerInviteDisable)
from openstadia_hub.schemas.user_server_role import UserServerRole
from openstadia_hub.services.server_invite import can_activate_server_invite_by_user
from openstadia_hub.services.server_permission import has_server_permission, ServerPermission

router = APIRouter(
    prefix="/servers/{server_id}/invites",
    tags=["servers_invites"],
)


@router.get("/", response_model=List[ServerInvite])
async def get_server_invites_(
        server_id: int,
        user: DbUser,
        db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.READ_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_server_invites(db, server_id)


@router.post("/", response_model=ServerInvite)
async def create_server_invite_(
        server_id: int,
        user: DbUser,
        db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.WRITE_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return create_server_invite(db, user.id, server_id)


@router.post("/info", response_model=ServerInviteInfo)
async def get_server_invite_info(
        token: ServerInviteToken,
        user: DbUser,
        db: DbSession
):
    server_invite = get_server_invite_by_token(db, token.token)
    if server_invite is None:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    can_activate = can_activate_server_invite_by_user(db, server_invite, user.id)

    server_invite = ServerInvite.model_validate(server_invite)
    return ServerInviteInfo(**server_invite.model_dump(), can_activate=can_activate)


@router.post("/activate")
async def activate_server_invite_(
        token: ServerInviteToken,
        user: DbUser,
        db: DbSession
):
    server_invite = get_server_invite_by_token(db, token.token)
    if server_invite is None:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    can_activate = can_activate_server_invite_by_user(db, server_invite, user.id)
    if not can_activate:
        raise HTTPException(status_code=404, detail="Can't activate invite token")

    # TODO Make it in single transaction
    activate_server_invite(db=db, server_invite=server_invite, user_id=user.id)
    create_server_access(db=db, user_id=user.id, server_id=server_invite.server_id, role=UserServerRole.USER)


@router.post("/disable")
async def disable_server_invite_(
        invite_disable: ServerInviteDisable,
        user: DbUser,
        db: DbSession
):
    server_invite = get_server_invite_by_id(db, invite_disable.id)
    if server_invite is None:
        raise HTTPException(status_code=404, detail="Invalid server invite id")

    server_id = server_invite.server_id
    if not has_server_permission(db, user.id, server_id, ServerPermission.WRITE_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return disable_server_invite(db, server_invite)
