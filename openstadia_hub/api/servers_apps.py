from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from openstadia_hub.core.auth import get_user
from openstadia_hub.core.database import get_db, Session
from openstadia_hub.crud.server import get_server_by_id
from openstadia_hub.models.user import User
from openstadia_hub.schemas.app import App
from openstadia_hub.services.apps import apps_service

router = APIRouter(
    prefix="/servers/{server_id}/apps",
    tags=["servers_apps"],
)


@router.get("/", response_model=List[App])
async def get_apps(server_id: int,
                   user: Annotated[User, Depends(get_user)],
                   db: Annotated[Session, Depends(get_db)]
                   ):
    server = get_server_by_id(db, server_id)
    if server not in user.servers:
        raise HTTPException(status_code=404, detail="No such server")

    return server.apps


@router.get("/sync", response_model=List[str])
async def get_apps(server_id: int,
                   user: Annotated[User, Depends(get_user)],
                   db: Annotated[Session, Depends(get_db)]
                   ) -> List[App]:
    server = get_server_by_id(db, server_id)
    if server not in user.servers:
        raise HTTPException(status_code=404, detail="No such server")

    apps = await apps_service.get_apps(server_id)
    if apps is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    return apps.apps
