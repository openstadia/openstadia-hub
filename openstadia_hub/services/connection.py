import asyncio
import random
from typing import Any, Optional, Dict

from fastapi import WebSocket

from openstadia_hub.schemas.packet import Packet, PacketType, PacketId, Header

ClientId = int


class ConnectionManager:
    def __init__(self):
        self.clients: dict[ClientId, WebSocket] = {}
        self.responses: dict[ClientId, dict[PacketId, asyncio.Future]] = {}

    async def connect(self, client_id: ClientId, websocket: WebSocket):
        await websocket.accept()
        self.clients[client_id] = websocket
        self.responses[client_id] = {}

    def disconnect(self, client_id: ClientId):
        self.clients.pop(client_id)

        pending_responses = self.responses.pop(client_id)
        for _, response in pending_responses.items():
            response.cancel()

    def is_connected(self, client_id: ClientId):
        return client_id in self.clients

    async def send_message(self, client_id: ClientId, message: str):
        websocket = self.clients.get(client_id)
        if websocket is None:
            return

        await websocket.send_text(message)

    async def send_request(self, client_id: ClientId, name: str, data: Any = {},
                           timeout: Optional[float] = None) -> Any:
        websocket = self.clients.get(client_id)
        if websocket is None:
            return None

        packet_id = random.randint(0, 1_000_000)
        response_future = asyncio.Future()
        self.responses[client_id][packet_id] = response_future

        header = Header(
            type=PacketType.EVENT,
            id=packet_id,
            name=name
        )

        packet = Packet(
            header=header,
            payload=data
        )

        await websocket.send_text(packet.encode())

        try:
            await asyncio.wait_for(response_future, timeout=timeout)
        except asyncio.TimeoutError:
            print('Timeout reached in request')

        response = None
        try:
            response = self.responses[client_id][packet_id].result()
        except BaseException:
            print('Future taken result error')

        return response

    def register_response(self, client_id: ClientId, packet_id: PacketId, message: Dict):
        try:
            response_future = self.responses[client_id][packet_id]
            response_future.set_result(message)
        except Exception:
            print('Exception when register response')


connection_manager = ConnectionManager()
