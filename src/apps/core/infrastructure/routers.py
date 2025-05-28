from fastapi import APIRouter

from apps.core.services import CourseService, QuestionService
from apps.core.infrastructure import schemas

router = APIRouter(prefix='/core')


@router.get('/courses/', response_model=list[schemas.CourseWithMemberCount], tags=['10.1'])
async def get_courses_with_member_count():
    return await CourseService.get_courses_with_member_count()


@router.get("/questions/{question_id}/", response_model=schemas.QuestionSchemaBase, tags=['9'])
async def get_question(question_id: int):
    return await QuestionService.get(question_id)


@router.post("/questions/", response_model=schemas.QuestionSchemaBase, tags=['9'])
async def create_question(item: schemas.QuestionSchemaCreate):
    return await QuestionService.create(item.model_dump())


@router.put("/questions/{question_id}/", response_model=schemas.QuestionSchemaBase, tags=['9'])
async def update_question(item: schemas.QuestionSchemaUpdate, question_id: int):
    return await QuestionService.update(item.model_dump(exclude_unset=True), question_id)


@router.delete("/questions/{question_id}/", tags=['9'])
async def update_question(question_id: int):
    await QuestionService.delete(question_id)


@router.get('/courses/', tags=['10.2'])
async def get_course_structure_analysis():
    return await CourseService.get_course_structure_analysis()
