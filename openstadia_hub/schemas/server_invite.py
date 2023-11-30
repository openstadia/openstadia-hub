from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServerInvite(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    token: str
    activated: bool

    created_at: datetime
    expiration_date: datetime
    activated_at: Optional[datetime]

    created_by: int
    server_id: int
    activated_by: Optional[int]


class ServerInviteInfo(ServerInvite):
    can_activate: bool


class ServerInviteToken(BaseModel):
    token: str


class ServerInviteDisable(BaseModel):
    id: int
