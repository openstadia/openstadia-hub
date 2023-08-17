from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud import server as crud
from openstadia_hub.schemas import server as schemas
from openstadia_hub.services.connection import connection_manager

router = APIRouter(
    prefix="/servers",
    tags=["apps"],
)


@router.post("/", response_model=schemas.Server)
def create_server_for_user(
        server: schemas.ServerCreate, user: DbUser, db: DbSession
):
    user_id = user.id
    return crud.create_user_server(db=db, server=server, user_id=user_id)


@router.get("/")
async def get_user_servers(user: DbUser):
    return user.servers


@router.get("/{server_id}")
async def get_server(
        server_id: int, user: DbUser, db: DbSession
):
    if not crud.has_server_access(db, user.id, server_id):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    return crud.get_server_by_id(db, server_id)


@router.get("/{server_id}/online", response_model=bool)
async def is_server_online(
        server_id: int, user: DbUser, db: DbSession
):
    if not crud.has_server_access(db, user.id, server_id):
        raise HTTPException(status_code=404, detail="Invalid access to server")

    is_online = connection_manager.is_connected(server_id)
    return is_online
