from typing import Annotated, Any, Union, Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.user import get_user_by_auth_id
from openstadia_hub.models import User
from .json_web_token import JsonWebToken

get_bearer_token = HTTPBearer()
AuthCredentials = Annotated[Optional[HTTPAuthorizationCredentials], Depends(get_bearer_token)]
AuthHeader = Annotated[Union[str, None], Header()]


def validate_token(token: AuthCredentials):
    return JsonWebToken(token.credentials).validate()


JwtUser = Annotated[Any, Depends(validate_token)]


def get_user(jwt_user: JwtUser, db: DbSession) -> User:
    auth_id = jwt_user.get('sub')
    user = get_user_by_auth_id(db, auth_id)
    if user is None:
        raise HTTPException(status_code=403, detail='User not found')
    return user


class PermissionsValidator:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, token: JwtUser):
        token_permissions = token.get("permissions")
        token_permissions_set = set(token_permissions)
        required_permissions_set = set(self.required_permissions)

        if not required_permissions_set.issubset(token_permissions_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )


DbUser = Annotated[User, Depends(get_user)]
