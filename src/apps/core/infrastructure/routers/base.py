from apps.core import services
from apps.core.infrastructure import schemas
from fastapi import APIRouter

router = APIRouter(prefix='/base')


@router.get('/members/', response_model=list[schemas.MemberListSchema])
async def get_all_members():
    return await services.MemberService.get_all()


@router.get('/courses/with-members-stats/', response_model=list[schemas.CourseWithMemberStats], tags=['10.2'])
async def get_courses_with_member_stats():
    return await services.CourseService.get_courses_with_member_stats()


@router.get('/modules/lesson-counts/', response_model=list[schemas.ModuleListSchema], tags=['10.2'])
async def get_modules_with_lesson_counts():
    return await services.ModuleService.get_with_lesson_counts()


@router.get('/lessons/', response_model=list[schemas.LessonListSchema])
async def get_all_lessons():
    return await services.LessonService.get_all()


@router.get('/questions/', response_model=list[schemas.QuestionListSchema], tags=['9', '11'])
async def get_all_questions():
    return await services.QuestionService.get_all()


@router.get('/questions/{question_id}/', response_model=schemas.QuestionSchemaBase, tags=['9'])
async def get_question(question_id: int):
    return await services.QuestionService.get(question_id)


@router.post('/questions/', response_model=schemas.QuestionSchemaBase, tags=['9'])
async def create_question(item: schemas.QuestionSchemaCreate):
    return await services.QuestionService.create(item.model_dump())


@router.put('/questions/{question_id}/', response_model=schemas.QuestionSchemaBase, tags=['9', '11'])
async def update_question(item: schemas.QuestionSchemaUpdate, question_id: int):
    return await services.QuestionService.update(item.model_dump(exclude_unset=True), question_id)


@router.delete('/questions/{question_id}/', tags=['9'])
async def delete_question(question_id: int):
    await services.QuestionService.delete(question_id)
