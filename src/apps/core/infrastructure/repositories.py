from typing import Type

from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from apps.core.infrastructure import models
from infrastructure.db.config import engine
from infrastructure.repositories import BaseRepository


class CourseRepository(BaseRepository):
    @staticmethod
    async def get_courses_with_member_count():
        statement = (
            select(
                models.CourseModel.id, models.CourseModel.name, func.count(models.MemberModel.id).label('members_count')
            )
            .join(models.MemberModel)
            .group_by(models.CourseModel.id)
        )

        async with AsyncSession(engine) as session:
            result = await session.exec(statement)

        return result.all()

    @property
    def model(self) -> Type[models.CourseModel]:
        return models.CourseModel


class QuestionRepository(BaseRepository):
    @property
    def model(self) -> Type[models.QuestionModel]:
        return models.QuestionModel
