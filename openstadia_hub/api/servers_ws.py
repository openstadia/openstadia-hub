from typing import Dict

from fastapi import APIRouter, Depends, WebSocket, WebSocketException, status, WebSocketDisconnect
from pydantic import ValidationError
from sqlalchemy.orm import Session

from openstadia_hub.core.auth import AuthHeader
from openstadia_hub.core.database import get_db
from openstadia_hub.crud.server import get_server_by_token
from openstadia_hub.schemas.packet import Packet, PacketType
from openstadia_hub.services.connection import connection_manager

router = APIRouter(
    prefix="/ws",
    tags=["servers_ws"],
)


@router.websocket("/")
async def websocket_endpoint(
        websocket: WebSocket,
        authorization: AuthHeader,
        db: Session = Depends(get_db)
):
    server = get_server_by_token(db, authorization)

    if server is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    server_id = server.id

    if connection_manager.is_connected(server_id):
        raise WebSocketException(code=status.WS_1000_NORMAL_CLOSURE, reason="Server already connected")

    await connection_manager.connect(server_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()

            try:
                packet = Packet.decode(data, Dict)
            except ValidationError:
                print("Receive wrong packet format")
                continue

            header = packet.header

            if header.type == PacketType.ACK:
                connection_manager.register_response(server_id, header.id, packet.payload)
    except WebSocketDisconnect:
        connection_manager.disconnect(server_id)
