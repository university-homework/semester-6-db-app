from abc import ABC, abstractmethod
from typing import Iterable, Type

from infrastructure.db.config import engine
from sqlalchemy.engine.result import ScalarResult
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseRepository(ABC):
    async def add(self, data: dict) -> SQLModel:
        instance = self.model(**data)
        async with AsyncSession(engine) as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        return instance

    async def get(
        self, conditions: dict | None = None, relations: Iterable = (), is_single: bool = False
    ) -> ScalarResult:
        conditions = (
            [getattr(self.model, field) == value for field, value in conditions.items()] if conditions else None
        )
        relations = [getattr(self.model, relation) for relation in relations]

        statement = select(self.model)
        for relation in relations:
            statement = statement.options(selectinload(relation))
        if conditions:
            statement = statement.where(*conditions)
        statement = statement.order_by(self.model.id)

        async with AsyncSession(engine) as session:
            result = await session.exec(statement)

        return result.first() if is_single else result.all()

    async def update(self, data: dict, instance_id: int) -> SQLModel:
        async with AsyncSession(engine) as session:
            instance = await session.get(self.model, instance_id)

            for key, value in data.items():
                setattr(instance, key, value)

            session.add(instance)
            await session.commit()
            await session.refresh(instance)

        return instance

    async def delete(self, instance_id: int) -> None:
        async with AsyncSession(engine) as session:
            instance = await session.get(self.model, instance_id)
            await session.delete(instance)
            await session.commit()

    async def get_amount(self) -> int:
        async with AsyncSession(engine) as session:
            statement = select(self.model)
            instances = await session.exec(statement)
        return len(instances.all())

    @property
    @abstractmethod
    def model(self) -> Type[SQLModel]:
        return  # noqa
