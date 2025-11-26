import pytest
from rest_framework.test import APIClient
from main.models import Question, Answer


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def question(db) -> Question:
    return Question.objects.create(text='Тестовый вопрос')


@pytest.fixture
def answer(db, question: Question) -> Answer:
    return Answer.objects.create(
        question_id=question,
        user_id='test-user-uuid',
        text='Тестовый ответ'
    )

