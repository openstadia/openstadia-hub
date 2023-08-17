from typing import Annotated, Any

from fastapi import APIRouter, Depends

from openstadia_hub.core.auth import get_user
from openstadia_hub.core.database import get_db, Session
from openstadia_hub.crud.apps import get_apps

router = APIRouter(
    prefix="/apps",
    tags=["apps"],
)


@router.get("/")
async def get_user_servers_lazy(
        user: Annotated[Any, Depends(get_user)],
        db: Session = Depends(get_db)
):
    return get_apps(db=db, user_id=user.id)
