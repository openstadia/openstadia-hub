from pydantic import BaseModel, ConfigDict

from openstadia_hub.schemas.user_server_role import UserServerRole


class ServerAccess(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    server_id: int
    role: UserServerRole
