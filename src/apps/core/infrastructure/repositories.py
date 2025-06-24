from typing import Type

from apps.core.infrastructure import models
from infrastructure.db.config import engine
from infrastructure.repositories import BaseRepository
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession


class MemberRepository(BaseRepository):
    @property
    def model(self) -> Type[models.MemberModel]:
        return models.MemberModel


class CourseRepository(BaseRepository):
    @staticmethod
    async def get_courses_with_member_stats():
        async with AsyncSession(engine) as session:
            total_members = await session.scalar(select(func.count(models.MemberModel.id)))

        statement = (
            select(
                models.CourseModel.id,
                models.CourseModel.name,
                func.count(models.MemberModel.id).label('member_count'),
                (func.count(models.MemberModel.id) / total_members * 100).label('percentage'),
            )
            .join(models.MemberModel, models.MemberModel.course_id == models.CourseModel.id)
            .group_by(models.CourseModel.id, models.CourseModel.name)
        )

        async with AsyncSession(engine) as session:
            result = await session.exec(statement)

        return result.all()

    @property
    def model(self) -> Type[models.CourseModel]:
        return models.CourseModel


class ModuleRepository(BaseRepository):
    @staticmethod
    async def get_with_lesson_counts():
        statement = (
            select(
                models.ModuleModel.id,
                models.ModuleModel.name,
                func.count(models.LessonModel.id).label('lesson_count'),
                func.rank().over(order_by=func.count(models.LessonModel.id).desc()).label('rank'),
            )
            .join(models.LessonModel, models.LessonModel.module_id == models.ModuleModel.id)
            .group_by(models.ModuleModel.id, models.ModuleModel.name)
        )

        async with AsyncSession(engine) as session:
            result = await session.exec(statement)

        return result.all()

    @property
    def model(self) -> Type[models.ModuleModel]:
        return models.ModuleModel


class LessonRepository(BaseRepository):
    @property
    def model(self) -> Type[models.LessonModel]:
        return models.LessonModel


class QuestionRepository(BaseRepository):
    @property
    def model(self) -> Type[models.QuestionModel]:
        return models.QuestionModel
