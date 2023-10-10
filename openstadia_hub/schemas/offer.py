import enum

from pydantic import BaseModel

from .session_description import SessionDescription


class CodecType(str, enum.Enum):
    vp8 = "vp8"
    vp9 = "vp9"
    openh264 = "openh264"
    x264 = "x264"


class Codec(BaseModel):
    type: str
    bitrate: int


class OfferApp(BaseModel):
    name: str


class Offer(SessionDescription):
    app: OfferApp
    codec: Codec
