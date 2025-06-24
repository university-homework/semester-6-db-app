import json
import random
from typing import Dict

from faker import Faker

fake = Faker('ru_RU')


def generate_test_data() -> Dict:
    data = {
        'users': [],
        'courses': [],
        'members': [],
        'modules': [],
        'lessons': [],
        'questions': [],
        'answer_options': [],
        'answers': [],
    }

    # 1. Генерируем 20 пользователей
    for _ in range(20):
        data['users'].append(
            {
                'username': fake.unique.user_name(),
                'password': fake.password(length=12),
                'last_name': fake.last_name(),
                'first_name': fake.first_name(),
                'patronymic': fake.middle_name() if random.random() > 0.3 else None,
            }
        )

    # 2. Генерируем 15 курсов
    for _ in range(15):
        data['courses'].append({'name': fake.catch_phrase()})

    # 3. Участники (по 1-3 курса на пользователя)
    for user_idx in range(len(data['users'])):
        for _ in range(random.randint(1, 3)):
            data['members'].append(
                {
                    'user_id': user_idx + 1,
                    'course_id': random.randint(1, len(data['courses'])),
                    'status': random.choice(['not_started', 'in_progress', 'completed']),
                }
            )

    # 4. Модули (по 3-6 на курс)
    for course_idx in range(len(data['courses'])):
        for i in range(random.randint(3, 6)):
            data['modules'].append({'course_id': course_idx + 1, 'name': f'Модуль {i + 1}: {fake.bs()}'})

    # 5. Уроки (по 4-8 на модуль)
    for module_idx in range(len(data['modules'])):
        for i in range(random.randint(4, 8)):
            data['lessons'].append(
                {
                    'module_id': module_idx + 1,
                    'name': f'Урок {i + 1}: {fake.sentence(nb_words=3)}',
                    'file_path': f'/lessons/{fake.uuid4()}.mp4',
                }
            )

    # 6. Вопросы (по 3-5 на урок)
    for lesson_idx in range(len(data['lessons'])):
        for i in range(random.randint(3, 5)):
            data['questions'].append(
                {'lesson_id': lesson_idx + 1, 'content': f'Вопрос {i + 1}: {fake.sentence(nb_words=8)}?'}
            )

    # 7. Варианты ответов (по 4 на вопрос, 1 правильный)
    for question_idx in range(len(data['questions'])):
        correct_index = random.randint(0, 3)
        for i in range(4):
            data['answer_options'].append(
                {
                    'question_id': question_idx + 1,
                    'content': f'Вариант {i + 1}: {fake.sentence(nb_words=5)}',
                    'is_right': i == correct_index,
                }
            )

    return data


if __name__ == '__main__':
    with open('test_data.json', 'w', encoding='utf-8') as f:
        json.dump(generate_test_data(), f, ensure_ascii=False, indent=2)
