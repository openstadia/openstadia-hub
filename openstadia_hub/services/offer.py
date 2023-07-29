from typing import Optional

from openstadia_hub.schemas.offer import Offer
from openstadia_hub.schemas.session_description import SessionDescription
from .connection import ConnectionManager, connection_manager


class OfferService:
    REQUEST_NAME = "OFFER"

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    async def send_offer(self, server_id: int, offer: Offer) -> Optional[SessionDescription]:
        answer_obj = await self.connection_manager.send_request(server_id, self.REQUEST_NAME, offer)
        if answer_obj is None:
            return None

        return SessionDescription.parse_obj(answer_obj)


offer_service = OfferService(connection_manager)
