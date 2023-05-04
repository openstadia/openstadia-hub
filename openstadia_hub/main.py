from typing import Union, Annotated

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
    Depends,
    Header,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .client_manager import ClientManager
from .connection_manager import ConnectionManager
from .packet import Packet, PacketType
from .session_description import SessionDescription

app = FastAPI()


async def get_token(
        websocket: WebSocket,
        authorization: Annotated[Union[str, None], Header()] = None,
):
    if authorization is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return authorization


connection_manager = ConnectionManager()
client_manager = ClientManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/offer/{client_id}")
async def offer(client_id: str, description: SessionDescription) -> SessionDescription:
    answer_obj = await connection_manager.send_request(client_id, description, timeout=None)
    if answer_obj is None:
        raise HTTPException(status_code=404, detail="Error with client answer")

    return SessionDescription.parse_obj(answer_obj)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Annotated[str, Depends(get_token)]):
    client = client_manager.get_client_by_token(token)
    if client is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    client_id = client.id

    if connection_manager.is_connected(client_id):
        raise WebSocketException(code=status.WS_1000_NORMAL_CLOSURE, reason="Client already connected")

    await connection_manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()

            try:
                packet = Packet.parse_raw(data)
            except ValidationError:
                print("Receive wrong packet format")
                continue

            if packet.type == PacketType.ACK:
                connection_manager.register_response(client_id, packet.id, packet.data)
    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
