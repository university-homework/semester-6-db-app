from sqlmodel import Field, Relationship

from infrastructure.db.models import BaseModel


class MemberModel(BaseModel, table=True):
    __tablename__ = 'members'

    id: int | None = Field(None, primary_key=True)
    user_id: int = Field(foreign_key='users.id')
    course_id: int = Field(foreign_key='courses.id')
    status: str

    user: 'UserModel' = Relationship(back_populates='members')
    course: 'CourseModel' = Relationship(back_populates='members')


class CourseModel(BaseModel, table=True):
    __tablename__ = 'courses'

    id: int | None = Field(None, primary_key=True)
    name: str

    members: list[MemberModel] = Relationship(back_populates='course')
    modules: list['ModuleModel'] = Relationship(back_populates='course')


class ModuleModel(BaseModel, table=True):
    __tablename__ = 'modules'

    id: int | None = Field(None, primary_key=True)
    course_id: int = Field(foreign_key='courses.id')
    name: str

    course: CourseModel = Relationship(back_populates='modules')
    lessons: list['LessonModel'] = Relationship(back_populates='module')


class LessonModel(BaseModel, table=True):
    __tablename__ = 'lessons'

    id: int | None = Field(None, primary_key=True)
    module_id: int = Field(foreign_key='modules.id')
    name: str
    file_path: str

    module: ModuleModel = Relationship(back_populates='lessons')
    questions: list['QuestionModel'] = Relationship(back_populates='lesson')


class QuestionModel(BaseModel, table=True):
    __tablename__ = 'questions'

    id: int | None = Field(None, primary_key=True)
    lesson_id: int = Field(foreign_key='lessons.id')
    content: str

    lesson: LessonModel = Relationship(back_populates='questions')
    answer_options: list['AnswerOptionModel'] = Relationship(cascade_delete=True, back_populates='question')


class AnswerOptionModel(BaseModel, table=True):
    __tablename__ = 'answer_options'

    id: int | None = Field(None, primary_key=True)
    question_id: int = Field(foreign_key='questions.id')
    content: str
    is_right: bool

    question: QuestionModel = Relationship(back_populates='answer_options')
