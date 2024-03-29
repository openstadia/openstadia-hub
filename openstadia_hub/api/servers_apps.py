from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.apps import get_apps_by_server_id
from openstadia_hub.schemas.app import App
from openstadia_hub.services.apps import apps_service, convert_to_apps
from openstadia_hub.services.server_permission import has_server_permission, ServerPermission

router = APIRouter(
    prefix="/servers/{server_id}/apps",
    tags=["servers_apps"],
)


@router.get("/", response_model=List[App])
async def get_apps(
        server_id: int,
        user: DbUser,
        db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.CONNECT):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_apps_by_server_id(db, server_id)


@router.get("/sync", response_model=List[App])
async def get_apps(
        server_id: int,
        user: DbUser,
        db: DbSession
):
    if not has_server_permission(db, user.id, server_id, ServerPermission.CONNECT):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    answer_apps = await apps_service.get_apps(server_id)
    if answer_apps is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    apps = convert_to_apps(answer_apps, server_id=server_id)
    return apps
