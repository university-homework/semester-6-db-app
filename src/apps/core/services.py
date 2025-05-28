from apps.core.infrastructure import repositories


class CourseService:
    @staticmethod
    async def get_courses_with_member_count():
        return await repositories.CourseRepository().get_courses_with_member_count()

    @staticmethod
    async def get_course_structure_analysis():
        return await repositories.CourseRepository().get_course_structure_analysis()


class QuestionService:
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
