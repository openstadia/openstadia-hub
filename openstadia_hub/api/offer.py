from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from openstadia_hub.core.auth import get_user
from openstadia_hub.core.database import get_db, Session
from openstadia_hub.crud.server import get_server_by_id
from openstadia_hub.models.user import User
from openstadia_hub.schemas.offer import Offer
from openstadia_hub.schemas.session_description import SessionDescription
from openstadia_hub.services.offer import offer_service

router = APIRouter(
    prefix="/servers/{server_id}/offer",
    tags=["offer"],
)


@router.post("/", response_model=SessionDescription)
async def handle_offer(server_id: int,
                       offer: Offer,
                       user: Annotated[User, Depends(get_user)],
                       db: Annotated[Session, Depends(get_db)]
                       ) -> SessionDescription:
    server = get_server_by_id(db, server_id)
    if server not in user.servers:
        raise HTTPException(status_code=404, detail="No such server")

    answer = await offer_service.send_offer(server_id, offer)
    if answer is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    return answer
