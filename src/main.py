from fastapi import FastAPI

from apps.core.infrastructure.routers import router as core_router
from apps.users.infrastructure.routers import router as users_router

app = FastAPI()

app.include_router(core_router)
app.include_router(users_router)
