from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser, UserInfo
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud.user import get_user_by_uniques, create_user
from openstadia_hub.schemas.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=User)
async def get_me(user: DbUser):
    return user


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: DbSession, jwt_user: UserInfo):
    if not jwt_user.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email not verified")

    email = jwt_user.get('email')
    auth_id = jwt_user.get('sub')

    db_user = get_user_by_uniques(
        db=db,
        username=user.username,
        auth_id=auth_id,
        email=email
    )
    if db_user:
        raise HTTPException(status_code=400, detail="User with this credentials already exists")

    return create_user(db=db, user=user, auth_id=auth_id, email=email)
