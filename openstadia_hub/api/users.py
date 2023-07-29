from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openstadia_hub import crud, schemas
from openstadia_hub.core.auth import get_user
from openstadia_hub.core.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
async def get_me(user: Annotated[Any, Depends(get_user)]):
    return user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
