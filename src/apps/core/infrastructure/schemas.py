from infrastructure.db.models import BaseModel


class MemberListSchema(BaseModel):
    id: int
    user_id: int
    course_id: int
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


class LessonListSchema(BaseModel):
    id: int
    module_id: int
    name: str
    file_path: str


class QuestionSchemaBase(BaseModel):
    id: int
    lesson_id: int
    content: str


class QuestionSchemaCreate(BaseModel):
    lesson_id: int
    content: str


class QuestionSchemaUpdate(QuestionSchemaCreate):
    lesson_id: int | None = None
    content: str | None = None
