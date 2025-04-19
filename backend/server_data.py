# База данных пользователей
users = [
    {"name": "Серега Пират"},
    {"name": "Алишер Моргенштерн"},
    {"name": "Олег Данилов"},
    {"name": "Антон Балов"}
]

# Баллы пользователей
users_score = [
    {"name": "Серега Пират", "course": 2, "direction": "AI", "marks": {"python": 4, "math": 3}},
    {"name": "Алишер Моргенштерн", "course": 1, "direction": "DEV", "marks": {"java": 3, "math": 5}},
    {"name": "Олег Данилов", "course": 1, "direction": "DATA", "marks": {"python": 5, "economics": 5}},
    {"name": "Антон Балов", "course": 1, "direction": "DEV", "marks": {"java": 2, "math": 4}}
]

tasks = {
    1: {  # Общие задания для 1 курса
        "common": [
            {
                "title": "Основы программирования",
                "description": "Написать программу 'Hello World' на любом языке"
            },
            {
                "title": "Математический анализ",
                "description": "Решить 5 задач по пределам функций"
            }
        ]
    },
    2: {  # Специализированные задания для 2 курса
        "AI": [
            {
                "title": "Нейронные сети",
                "description": "Реализовать перцептрон для задачи классификации"
            },
            {
                "title": "Сделать новый язык программирования",
                "description": "Напишите форк c++ который норм реализован"
            },
            {
                "title": "Посмотреть лекцию",
                "description": "Посмотреть лекцию про то как быть лучшим в своем деле"
            }
        ],
        "DEV": [
            {
                "title": "Веб-разработка",
                "description": "Создать простое веб-приложение на Flask"
            }
        ],
        "DATA": [
            {
                "title": "Анализ данных",
                "description": "Проанализировать датасет с помощью Pandas"
            }
        ]
    }
}