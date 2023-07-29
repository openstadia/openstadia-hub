from fastapi import APIRouter, HTTPException

from openstadia_hub.schemas.offer import Offer
from openstadia_hub.schemas.session_description import SessionDescription
from openstadia_hub.services.offer import offer_service

router = APIRouter(
    prefix="/servers/{server_id}/offer",
    tags=["offer"],
)


@router.post("/", response_model=SessionDescription)
async def handle_offer(server_id: int, offer: Offer) -> SessionDescription:
    # TODO Add user validation
    answer = await offer_service.send_offer(server_id, offer)
    if answer is None:
        raise HTTPException(status_code=404, detail="Error with server answer")

    return answer
