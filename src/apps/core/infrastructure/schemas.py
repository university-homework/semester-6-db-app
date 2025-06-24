from infrastructure.db.models import BaseModel
from apps.users.infrastructure.schemas import UserReadSchema


class CourseForMemberResponseSchema(BaseModel):
    name: str


class MemberListSchema(BaseModel):
    id: int
    user: UserReadSchema
    course: CourseForMemberResponseSchema
    status: str


class CourseWithMemberStats(BaseModel):
    id: int
    name: str
    member_count: int
    percentage: float


class ModuleListSchema(BaseModel):
    id: int
    name: str
    lesson_count: int
    rank: int


class ModuleResponseForLessonSchema(BaseModel):
    name: str


class LessonListSchema(BaseModel):
    id: int
    module: ModuleResponseForLessonSchema
    name: str
    file_path: str


class QuestionSchemaBase(BaseModel):
    id: int
    lesson_id: int
    content: str


class ListResponseForQuestionSchema(BaseModel):
    name: str


class QuestionListSchema(BaseModel):
    id: int
    lesson: ListResponseForQuestionSchema
    content: str


class QuestionSchemaCreate(BaseModel):
    lesson_id: int
    content: str


class QuestionSchemaUpdate(QuestionSchemaCreate):
    lesson_id: int | None = None
    content: str | None = None
