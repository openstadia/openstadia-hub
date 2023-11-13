from typing import Optional, List

from pydantic import BaseModel

from openstadia_hub.schemas.app import App
from .connection import ConnectionManager, connection_manager


class AppAnswer(BaseModel):
    id: int
    name: str


class AppsAnswer(BaseModel):
    apps: List[AppAnswer]


class AppsService:
    REQUEST_NAME = "APPS"

    def __init__(self, conn_manager: ConnectionManager):
        self.connection_manager = conn_manager

    async def get_apps(self, server_id: int) -> Optional[AppsAnswer]:
        apps = await self.connection_manager.send_request(server_id, self.REQUEST_NAME)
        if apps is None:
            return None

        return AppsAnswer.model_validate(apps)


def convert_to_apps(apps_answer: AppsAnswer, server_id: int) -> List[App]:
    apps = []

    for answer_app in apps_answer.apps:
        app = App(
            id=answer_app.id,
            name=answer_app.name,
            server_id=server_id
        )
        apps.append(app)

    return apps


apps_service = AppsService(connection_manager)
