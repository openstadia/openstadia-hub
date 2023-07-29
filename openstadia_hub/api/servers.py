from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from openstadia_hub import schemas
from openstadia_hub.core.auth import get_user
from openstadia_hub.core.database import get_db
from openstadia_hub.crud import server as crud

router = APIRouter(
    prefix="/servers",
    tags=["apps"],
)


@router.post("/", response_model=schemas.Server)
def create_server_for_user(
        item: schemas.ServerCreate, user: Annotated[Any, Depends(get_user)], db: Session = Depends(get_db)
):
    user_id = user.id
    return crud.create_user_server(db=db, item=item, user_id=user_id)


@router.get("/")
async def get_user_servers(user: Annotated[Any, Depends(get_user)]):
    return user.servers


@router.get("/{server_id}")
async def get_server(
        server_id: int, user: Annotated[Any, Depends(get_user)], db: Session = Depends(get_db)
):
    return crud.get_server_by_id(db, server_id)
