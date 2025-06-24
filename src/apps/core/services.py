from apps.core.infrastructure import repositories


class MemberService:
    @staticmethod
    async def get_all():
        return await repositories.MemberRepository().get(relations=('user', 'course'))


class CourseService:
    @staticmethod
    async def get_courses_with_member_stats():
        return await repositories.CourseRepository().get_courses_with_member_stats()


class ModuleService:
    @staticmethod
    async def get_all():
        return await repositories.ModuleRepository().get()

    @staticmethod
    async def get_with_lesson_counts():
        return await repositories.ModuleRepository().get_with_lesson_counts()


class LessonService:
    @staticmethod
    async def get_all():
        return await repositories.LessonRepository().get(relations=('module',))


class QuestionService:
    @staticmethod
    async def get_all():
        return await repositories.QuestionRepository().get(relations=('lesson',))

    @staticmethod
    async def get(question_id: int):
        conditions = {
            'id': question_id,
        }
        return await repositories.QuestionRepository().get(conditions, is_single=True)

    @staticmethod
    async def create(data: dict):
        return await repositories.QuestionRepository().add(data)

    @staticmethod
    async def update(data: dict, question_id: int):
        return await repositories.QuestionRepository().update(data, question_id)

    @staticmethod
    async def delete(question_id: int):
        return await repositories.QuestionRepository().delete(question_id)
