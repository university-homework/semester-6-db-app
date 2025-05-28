from fastapi import APIRouter

from apps.users.infrastructure.schemas import UserReadSchema
from apps.users.services import UserService

router = APIRouter(prefix='/users', tags=['10.1'])


@router.get('/{user_id}', response_model=UserReadSchema)
async def get_user_by_id(user_id: int):
    return await UserService.get_user_by_id(user_id)


@router.get('/', response_model=list[UserReadSchema])
async def get_all_users():
    return await UserService.get_all_users()
