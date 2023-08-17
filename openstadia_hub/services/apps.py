from typing import Optional, List

from pydantic import BaseModel

from .connection import ConnectionManager, connection_manager


class AppsAnswer(BaseModel):
    apps: List[str]


class AppsService:
    REQUEST_NAME = "APPS"

    def __init__(self, conn_manager: ConnectionManager):
        self.connection_manager = conn_manager

    async def get_apps(self, server_id: int) -> Optional[AppsAnswer]:
        apps = await self.connection_manager.send_request(server_id, self.REQUEST_NAME)
        if apps is None:
            return None

        return AppsAnswer.model_validate(apps)


apps_service = AppsService(connection_manager)
