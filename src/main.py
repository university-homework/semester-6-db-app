from apps.core.infrastructure.routers.additional import router as additional_router
from apps.core.infrastructure.routers.base import router as base_router
from apps.users.infrastructure.routers import router as users_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(base_router)
app.include_router(additional_router)
app.include_router(users_router)
