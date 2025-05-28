from typing import Type

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.users.infrastructure.models import UserModel
from infrastructure.db.config import engine
from infrastructure.repositories import BaseRepository


class UserRepository(BaseRepository):
    async def get_all_users(self):
        statement = select(self.model)

        async with AsyncSession(engine) as session:
            result = await session.exec(statement)

        return result.all()

    @property
    def model(self) -> Type[UserModel]:
        return UserModel
