from fastapi import APIRouter, HTTPException

from openstadia_hub.core.auth import DbUser, JwtUser
from openstadia_hub.core.database import DbSession
from openstadia_hub.crud import user as crud
from openstadia_hub.schemas import user as schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
async def get_me(user: DbUser):
    return user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: DbSession, jwt_user: JwtUser):
    if not jwt_user.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email not verified")

    email = jwt_user.get('email')
    auth_id = jwt_user.get('sub')

    db_user = crud.get_user_by_uniques(
        db=db,
        username=user.username,
        auth_id=auth_id,
        email=email
    )
    if db_user:
        raise HTTPException(status_code=400, detail="User with this credentials already exists")

    return crud.create_user(db=db, user=user, auth_id=auth_id, email=email)
