from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from openstadia_hub.api import offer, servers, users, servers_apps, servers_ws, apps

app = FastAPI()
app.include_router(servers_ws.router)
app.include_router(offer.router)
app.include_router(servers.router)
app.include_router(users.router)
app.include_router(servers_apps.router)
app.include_router(apps.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def allow_private_network(request: Request, call_next):
    response = await call_next(request)

    if request.headers.get('Access-Control-Request-Private-Network') == 'true':
        response.headers["Access-Control-Allow-Private-Network"] = "true"

    return response
