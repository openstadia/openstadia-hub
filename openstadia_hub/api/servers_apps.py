from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.apps import get_apps_by_server_id
from openstadia_hub.crud.server import has_server_access
from openstadia_hub.schemas.app import App, AppSync
from openstadia_hub.services.apps import apps_service

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
    if not has_server_access(db, user.id, server_id):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return get_apps_by_server_id(db, server_id)


@router.get("/sync", response_model=List[AppSync])
async def get_apps(
        server_id: int,
        user: DbUser,
        db: DbSession
) -> List[App]:
    if not has_server_access(db, user.id, server_id):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    answer_apps = await apps_service.get_apps(server_id)
    if answer_apps is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    apps = list(map(lambda app: AppSync(name=app), answer_apps.apps))

    return apps
