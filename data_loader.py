import json

from pydash import find

from data import data

DATA_PATH = 'data/data.json'


def create_data():
    print('data_loader run')
    # Сохраняем все данные в один словарь
    all_data = dict(goals=data.goals, teachers=data.teachers, weekdays=data.weekdays)

    # Создаём файл JSON
    with open(DATA_PATH, 'w') as f:
        json.dump(all_data, f, ensure_ascii=False)

    print('data loaded into', DATA_PATH)


def load_json(path) -> dict:
    """Загружает JSON-набор данных."""
    try:
        with open(path) as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        create_data()
        return load_json(path)


def get_all_teachers() -> list[dict]:
    """Загружает данные всех преподавателей."""
    return load_json(DATA_PATH)['teachers']


def get_teacher(teacher_id: int) -> dict:
    """Получает данные учителя по его id."""
    return find(get_all_teachers(), {'id': teacher_id})


def get_goals(teacher: dict = None, drop_emoji=False) -> dict:
    """Получает список целей. Если указан преподаватель, то получает только цели для преподавателя."""
    if teacher:
        return {k: v for k, v in get_goals(drop_emoji=drop_emoji).items() if k in teacher['goals']}

    all_data = load_json(DATA_PATH)
    return {k: v['name'] for k, v in all_data['goals'].items()} if drop_emoji else all_data['goals']


def get_weekdays() -> dict:
    """Загружает словарь с днями недели."""
    return load_json(DATA_PATH)['weekdays']