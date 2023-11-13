from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.server import (create_user_server, get_server_by_id, regenerate_server_token,
                                        delete_server_by_id, get_user_servers)
from openstadia_hub.schemas.server import Server, ServerCreate, ServerToken, ServerSettings
from openstadia_hub.schemas.server import ServerRole
from openstadia_hub.services.connection import connection_manager
from openstadia_hub.services.server_permission import has_server_permission, ServerPermission

router = APIRouter(
    prefix="/servers",
    tags=["servers"],
)


@router.post("/", response_model=Server)
def create_server_for_user(
        server: ServerCreate, user: DbUser, db: DbSession
):
    user_id = user.id
    db_server = create_user_server(db=db, server_create=server, user_id=user_id)
    return db_server


@router.get("/", response_model=List[ServerRole])
async def get_user_servers_(db: DbSession, user: DbUser):
    servers = get_user_servers(db, user.id)
    return servers


@router.get("/{server_id}", response_model=Server)
async def get_server(
        server_id: int, user: DbUser, db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.CONNECT):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_server_by_id(db, server_id)


@router.get("/{server_id}/settings", response_model=ServerSettings)
async def get_server_settings(
        server_id: int, user: DbUser, db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.READ_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_server_by_id(db, server_id)


@router.get("/{server_id}/online", response_model=bool)
async def is_server_online(
        server_id: int, user: DbUser, db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.CONNECT):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    is_online = connection_manager.is_connected(server_id)
    return is_online


@router.post("/{server_id}/token", response_model=ServerToken)
async def regenerate_server_token_(
        server_id: int, user: DbUser, db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.WRITE_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    db_server = regenerate_server_token(db, server_id)
    server_token = ServerToken(token=db_server.token)

    return server_token


@router.delete("/{server_id}", response_model=Server)
async def delete_server(
        server_id: int, user: DbUser, db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.WRITE_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return delete_server_by_id(db, server_id)
