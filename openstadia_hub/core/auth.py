from typing import Annotated, Any, Union

from fastapi import Depends, WebSocket, Header, WebSocketException, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from openstadia_hub import crud
from openstadia_hub.core.database import get_db
from .json_web_token import JsonWebToken

get_bearer_token = HTTPBearer()


async def get_token(
        websocket: WebSocket,
        authorization: Annotated[Union[str, None], Header()] = None,
):
    print(authorization)
    if authorization is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return authorization


def validate_token(token: str = Depends(get_bearer_token)):
    return JsonWebToken(token.credentials).validate()


def get_user(token: Annotated[str, Depends(validate_token)],
             db: Session = Depends(get_db)) -> Any:
    email = token.get('sub')
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=403)
    return user


class PermissionsValidator:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(validate_token)):
        token_permissions = token.get("permissions")
        token_permissions_set = set(token_permissions)
        required_permissions_set = set(self.required_permissions)

        if not required_permissions_set.issubset(token_permissions_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
