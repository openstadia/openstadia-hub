from fastapi import APIRouter

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.apps import get_apps_by_user_id

router = APIRouter(
    prefix="/apps",
    tags=["apps"],
)


@router.get("/")
async def get_apps_by_user(user: DbUser, db: DbSession):
    return get_apps_by_user_id(db=db, user_id=user.id)
