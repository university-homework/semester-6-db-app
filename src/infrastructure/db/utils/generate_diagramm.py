from apps.core.infrastructure.models import (  # noqa
    AnswerModel,
    AnswerOptionModel,
    CourseModel,
    LessonModel,
    MemberModel,
    ModuleModel,
    QuestionModel,
)
from apps.users.infrastructure.models import UserModel  # noqa
from eralchemy2 import render_er
from sqlmodel import SQLModel


def generate_from_models():
    output_file = 'er_diagram.png'

    render_er(SQLModel.metadata, output_file)
    print(f'Диаграмма сохранена в {output_file}')


if __name__ == '__main__':
    generate_from_models()
