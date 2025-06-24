import asyncio
import json

from apps.core.infrastructure import models as core_models
from apps.users.infrastructure import models as users_models
from consts import FIXTURES_ROOT
from infrastructure.db.config import engine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession


async def load_from_json(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    async with AsyncSession(engine) as session:
        await session.exec(text('SET CONSTRAINTS ALL DEFERRED'))

        for table, model in [
            (users_models.UserModel.__tablename__, users_models.UserModel),
            (core_models.CourseModel.__tablename__, core_models.CourseModel),
            (core_models.MemberModel.__tablename__, core_models.MemberModel),
            (core_models.ModuleModel.__tablename__, core_models.ModuleModel),
            (core_models.LessonModel.__tablename__, core_models.LessonModel),
            (core_models.QuestionModel.__tablename__, core_models.QuestionModel),
            (core_models.AnswerOptionModel.__tablename__, core_models.AnswerOptionModel),
        ]:
            for item in data.get(table, []):
                session.add(model(**item))

        await session.commit()


if __name__ == '__main__':
    asyncio.run(load_from_json(FIXTURES_ROOT / 'data.json'))
