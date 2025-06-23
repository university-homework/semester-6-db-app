from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.core.infrastructure.routers import router as core_router
from apps.users.infrastructure.routers import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core_router)
app.include_router(users_router)
