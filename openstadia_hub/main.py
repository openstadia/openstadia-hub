from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openstadia_hub.api import offer, servers, users, apps, servers_ws
from openstadia_hub.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(servers_ws.router)
app.include_router(offer.router)
app.include_router(servers.router)
app.include_router(users.router)
app.include_router(apps.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
