# Hightalent API

REST API сервис для работы с вопросами и ответами. Построен на Django REST Framework с JWT аутентификацией.

## Технологии

- Python 3.10
- Django 5.2
- Django REST Framework
- Simple JWT
- PostgreSQL 13
- Docker & Docker Compose

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Hightalent
```

### 2. Настройка переменных окружения

Создайте файл `APIservice/.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
LEVEL=PROD

# PostgreSQL
POSTGRES_DB=hightalent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. Запуск через Docker Compose

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8000

### 4. Остановка

```bash
docker-compose down
```

## API Endpoints

### Вопросы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/questions/` | Список всех вопросов |
| POST | `/questions/` | Создать вопрос |
| GET | `/questions/{id}/` | Получить вопрос с ответами |
| DELETE | `/questions/{id}/` | Удалить вопрос (каскадно с ответами) |

### Ответы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/questions/{id}/answers/` | Список ответов на вопрос |
| POST | `/questions/{id}/answers/` | Добавить ответ к вопросу |
| GET | `/answers/{id}/` | Получить ответ |
| DELETE | `/answers/{id}/` | Удалить ответ |

## Примеры запросов

### Создать вопрос

```bash
curl -X POST http://localhost:8000/questions/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Какой ваш любимый язык программирования?"}'
```

### Получить список вопросов

```bash
curl http://localhost:8000/questions/
```

### Получить вопрос с ответами

```bash
curl http://localhost:8000/questions/1/
```

### Добавить ответ

```bash
curl -X POST http://localhost:8000/questions/1/answers/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-123", "text": "Python!"}'
```

### Удалить вопрос (вместе с ответами)

```bash
curl -X DELETE http://localhost:8000/questions/1/
```

## Локальная разработка

### Установка зависимостей

```bash
cd APIservice
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Запуск сервера

```bash
python manage.py migrate
python manage.py runserver
```

### Запуск тестов

```bash
pip install pytest pytest-django
pytest -v
```

## Структура проекта

```
Hightalent/
├── APIservice/
│   ├── main/
│   │   ├── models.py       # Модели Question, Answer
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF сериализаторы
│   │   ├── urls.py         # Маршруты API
│   │   └── tests.py        # Тесты
│   ├── service/
│   │   └── settings/       # Настройки Django
│   ├── Dockerfile
│   └── manage.py
├── docker-compose.yaml
└── README.md
```
