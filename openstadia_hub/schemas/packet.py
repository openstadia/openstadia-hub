import enum
import json
from typing import Optional, Generic, TypeVar, Type

from pydantic import BaseModel, TypeAdapter

PayloadT = TypeVar('PayloadT')
PacketId = int


class PacketType(str, enum.Enum):
    EVENT = 'EVENT'
    ACK = 'ACK'


class Header(BaseModel):
    type: PacketType
    id: Optional[PacketId]
    name: str


SEPARATOR = '|'


class Packet(BaseModel, Generic[PayloadT]):
    header: Header
    payload: PayloadT

    def encode(self):
        header = self.header.json()
        if isinstance(self.payload, BaseModel):
            payload = self.payload.json()
        else:
            payload = json.dumps(self.payload)
        return header + SEPARATOR + payload

    @staticmethod
    def decode(data: str, payload_type: Type[PayloadT]) -> 'Packet[PayloadT]':
        parts = data.split(SEPARATOR)
        if len(parts) != 2:
            raise Exception('wrong number of packet parts')

        header = Header.model_validate_json(parts[0])
        payload = TypeAdapter(payload_type).validate_json(parts[1])

        return Packet(header=header, payload=payload)
