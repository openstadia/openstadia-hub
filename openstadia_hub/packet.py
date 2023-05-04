import enum
from typing import Any, Optional

from pydantic import BaseModel

PacketId = int


class PacketType(str, enum.Enum):
    EVENT = 'EVENT'
    ACK = 'ACK'


class Packet(BaseModel):
    type: PacketType
    data: Any
    id: Optional[PacketId]
