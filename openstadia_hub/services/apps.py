from typing import Optional, List

from pydantic import parse_obj_as

from openstadia_hub.schemas.app import App
from .connection import ConnectionManager, connection_manager


class AppsService:
    REQUEST_NAME = "APPS"

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    async def get_apps(self, server_id: int) -> Optional[List[App]]:
        apps = await self.connection_manager.send_request(server_id, self.REQUEST_NAME)
        if apps is None:
            return None

        return parse_obj_as(List[App], apps)


apps_service = AppsService(connection_manager)
