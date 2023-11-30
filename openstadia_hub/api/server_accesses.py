from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.server_access import get_server_accesses, delete_server_access
from openstadia_hub.schemas.server_access import ServerAccess
from openstadia_hub.services.server_permission import has_server_permission, ServerPermission

router = APIRouter(
    prefix="/servers/{server_id}/accesses",
    tags=["servers_accesses"],
)


@router.get("/", response_model=List[ServerAccess])
async def get_server_accesses_(
        server_id: int,
        user: DbUser,
        db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.READ_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_server_accesses(db=db, server_id=server_id)


@router.delete("/users/{user_id}", response_model=ServerAccess)
async def delete_server_access_(
        server_id: int,
        user: DbUser,
        db: DbSession,
        user_id: int
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.WRITE_SETTINGS):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    server_access = delete_server_access(db=db, user_id=user_id, server_id=server_id)
    if server_access is None:
        raise HTTPException(status_code=404, detail="Invalid server access")

    return server_access
