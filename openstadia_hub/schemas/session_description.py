import enum

from pydantic import BaseModel


class SDPType(str, enum.Enum):
    offer = "offer"
    pranswer = "pranswer"
    answer = "answer"
    rollback = "rollback"


class SessionDescription(BaseModel):
    type: str
    sdp: str
