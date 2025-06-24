from datetime import datetime

import pytz
from apps.core.infrastructure import models
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.db.config import get_db
from sqlmodel import exists, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(prefix='/additional')


@router.get('/system/stats')
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    """Статистика системы (общие цифры)"""

    courses_count = (await db.exec(select(func.count(models.CourseModel.id)))).one()
    modules_count = (await db.exec(select(func.count(models.ModuleModel.id)))).one()
    lessons_count = (await db.exec(select(func.count(models.LessonModel.id)))).one()
    questions_count = (await db.exec(select(func.count(models.QuestionModel.id)))).one()
    members_count = (await db.exec(select(func.count(models.MemberModel.id)))).one()

    return [
        {
            'courses': courses_count,
            'modules': modules_count,
            'lessons': lessons_count,
            'questions': questions_count,
            'members': members_count,
            'updated_at': datetime.now(pytz.timezone('Asia/Yekaterinburg')).strftime('%Y-%m-%d %H:%M:%S'),
        }
    ]


@router.get('/courses/most-popular')
async def get_most_popular_course(db: AsyncSession = Depends(get_db)):
    """Самый популярный курс (по количеству участников)"""

    result = (
        await db.exec(
            select(models.CourseModel, func.count(models.MemberModel.id).label('members_count'))
            .join(models.MemberModel, models.MemberModel.course_id == models.CourseModel.id)
            .group_by(models.CourseModel.id)
            .order_by(func.count(models.MemberModel.id).desc())
            .limit(1)
        )
    ).first()

    course, members_count = result

    return [
        {
            'course': course.name,
            'members_count': members_count,
        }
    ]


@router.get('/courses/richest-content')
async def get_course_with_richest_content(db: AsyncSession = Depends(get_db)):
    """Курс с наибольшим количеством учебного материала"""

    result = (
        await db.exec(
            select(models.CourseModel, func.count(models.LessonModel.id).label('lessons_count'))
            .join(models.ModuleModel, models.ModuleModel.course_id == models.CourseModel.id)
            .join(models.LessonModel, models.LessonModel.module_id == models.ModuleModel.id)
            .group_by(models.CourseModel.id)
            .order_by(func.count(models.LessonModel.id).desc())
            .limit(1)
        )
    ).first()

    course, lessons_count = result

    return [{'course': course.name, 'lessons_count': lessons_count}]


@router.get('/courses/without-modules')
async def get_courses_without_modules(db: AsyncSession = Depends(get_db)):
    """Курсы без модулей (возможно, нуждаются в доработке)"""

    courses = (
        await db.exec(
            select(models.CourseModel).where(~exists().where(models.ModuleModel.course_id == models.CourseModel.id))
        )
    ).all()

    return [{'course': course.name} for course in courses]


# @router.get('/questions/question-of-the-day')
# async def get_question_of_the_day(db: AsyncSession = Depends(get_db)):
#     """Случайный "вопрос дня" со всеми вариантами ответов"""
#
#     # Используем день года для псевдослучайного выбора, чтобы вопрос менялся раз в день
#     day_of_year = datetime.now().timetuple().tm_yday
#
#     question = (await db.exec(
#         select(models.QuestionModel)
#         .offset(day_of_year % select(func.count(models.QuestionModel.id)).scalar_subquery())
#         .limit(1)
#     )).first()
#
#     answers = (await db.exec(
#         select(models.AnswerOptionModel)
#         .where(models.AnswerOptionModel.question_id == question.id)
#         .order_by(models.AnswerOptionModel.id)
#     )).all()
#
#     return {
#         'question': question.content,
#         'answers': answers,
#     }


# @router.get('/questions/multiple-correct-answers')
# async def get_questions_with_multiple_correct_answers(db: AsyncSession = Depends(get_db)):
#     """Вопросы с несколькими правильными ответами"""
#
#     questions = (await db.exec(
#         select(models.QuestionModel, func.count(models.AnswerOptionModel.id).label('correct_answers_count'))
#         .join(models.AnswerOptionModel, models.AnswerOptionModel.question_id == models.QuestionModel.id)
#         .where(models.AnswerOptionModel.is_right == True)
#         .group_by(models.QuestionModel.id)
#         .having(func.count(models.AnswerOptionModel.id) > 1)
#     )).all()
#
#     return [{
#         'count': len(questions),
#         'questions': [{'question': q[0], 'correct_answers_count': q[1]} for q in questions],
#     }]


# 5. Распределение участников по статусам
# @router.get('/members/status-distribution')
# async def get_members_status_distribution(db: AsyncSession = Depends(get_db)):
#     results = db.exec(
#         select(models.MemberModel.status, func.count(models.MemberModel.id).label('count')).group_by(
#             models.MemberModel.status
#         )
#     ).all()
#
#     return {'distribution': dict(results), 'message': 'Members count grouped by status'}


# 6. Модули с необычно большим количеством уроков (выбросы)
# @router.get("/modules/outliers")
# async def get_modules_with_unusual_lesson_count(db: AsyncSession = Depends(get_db)):
#     # Сначала получаем среднее количество уроков в модуле
#     avg_lessons = db.exec(
#         select(
#             func.avg(lesson_count).label("avg")
#         ).from_(
#             select(
#                 models.ModuleModel.id,
#                 func.count(models.LessonModel.id).label("lesson_count")
#                 .join(models.LessonModel, models.LessonModel.module_id == models.ModuleModel.id)
#                 .group_by(models.ModuleModel.id)
#             )
#         ).one()
#
#     # Ищем модули с количеством уроков > 2*avg
#     outlier_modules = db.exec(
#         select(
#             models.ModuleModel,
#             func.count(models.LessonModel.id).label("lesson_count"),
#             models.CourseModel.name.label("course_name")
#         )
#         .join(models.LessonModel, models.LessonModel.module_id == models.ModuleModel.id)
#         .join(models.CourseModel, models.ModuleModel.course_id == models.CourseModel.id)
#         .group_by(models.ModuleModel.id, models.CourseModel.name)
#         .having(func.count(models.LessonModel.id) > 2 * avg_lessons)
#     ).all()
#
#     return {
#         "average_lessons_per_module": round(avg_lessons, 2),
#         "threshold": 2 * avg_lessons,
#         "outlier_modules": [{
#             "module": m[0],
#             "lesson_count": m[1],
#             "course_name": m[2]
#         } for m in outlier_modules]
#     }
