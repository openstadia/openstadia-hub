from typing import Union, Annotated, Any

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
    Depends,
    Header,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import ValidationError

from .auth.authorization_header_elements import get_bearer_token
from .client_manager import ClientManager
from .config import get_settings, Settings
from .connection_manager import ConnectionManager
from .packet import Packet, PacketType
from .session_description import SessionDescription

app = FastAPI()

request = requests.Request()
connection_manager = ConnectionManager()
client_manager = ClientManager()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_token(
        websocket: WebSocket,
        authorization: Annotated[Union[str, None], Header()] = None,
):
    if authorization is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return authorization


async def get_user(token: Annotated[str, Depends(get_bearer_token)],
                   settings: Annotated[Settings, Depends(get_settings)]) -> Any:
    id_info = id_token.verify_oauth2_token(token, request, settings.google_client_id)
    return id_info


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


@app.post("/servers", tags=["servers"])
async def create_server(user: Annotated[Any, Depends(get_user)]):
    pass


@app.get("/servers", tags=["servers"])
async def get_servers(user: Annotated[Any, Depends(get_user)]):
    return []


@app.get("/me")
async def get_me(user: Annotated[Any, Depends(get_user)]):
    user_id = user['sub']
    return user
