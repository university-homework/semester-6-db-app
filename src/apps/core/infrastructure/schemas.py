from infrastructure.db.models import BaseModel


class CourseWithMemberCount(BaseModel):
    id: int
    name: str
    members_count: int


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
