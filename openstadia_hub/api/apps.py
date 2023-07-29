from typing import List

from fastapi import APIRouter, HTTPException

from openstadia_hub.schemas.app import App
from openstadia_hub.services.apps import apps_service

router = APIRouter(
    prefix="/servers/{server_id}/apps",
    tags=["apps"],
)


@router.get("/", response_model=List[App])
async def get_apps(server_id: int) -> List[App]:
    # TODO Add user validation
    apps = await apps_service.get_apps(server_id)
    if apps is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    return apps
