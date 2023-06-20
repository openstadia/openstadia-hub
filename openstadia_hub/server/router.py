from fastapi import APIRouter

router = APIRouter()


@router.post("/getServers", tags=["servers"])
async def get_servers():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.post("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}