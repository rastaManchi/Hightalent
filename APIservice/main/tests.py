import pytest
from rest_framework import status
from main.models import Question, Answer


@pytest.mark.django_db
class TestQuestionList:
    def test_get_empty_list(self, api_client):
        response = api_client.get('/questions/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_list_with_questions(self, api_client, question):
        response = api_client.get('/questions/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == question.id
        assert data[0]['text'] == question.text
    
    def test_create_question(self, api_client):
        response = api_client.post(
            '/questions/',
            {'text': 'Новый вопрос'},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['text'] == 'Новый вопрос'
        assert Question.objects.filter(text='Новый вопрос').exists()
    
    def test_create_question_without_text(self, api_client):
        response = api_client.post('/questions/', {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_question_with_empty_text(self, api_client):
        response = api_client.post('/questions/', {'text': ''}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestQuestionDetail:
    def test_get_question(self, api_client, question):
        response = api_client.get(f'/questions/{question.id}/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == question.id
        assert data['text'] == question.text
        assert 'answers' in data
    
    def test_get_question_not_found(self, api_client, db):
        response = api_client.get('/questions/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_question(self, api_client, question):
        response = api_client.delete(f'/questions/{question.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Question.objects.filter(id=question.id).exists()
    
    def test_delete_question_cascades_answers(self, api_client, question, answer):
        answer_id = answer.id
        response = api_client.delete(f'/questions/{question.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(id=answer_id).exists()


@pytest.mark.django_db
class TestAnswerList:
    def test_get_empty_answers(self, api_client, question):
        response = api_client.get(f'/questions/{question.id}/answers/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_answers(self, api_client, question, answer):
        response = api_client.get(f'/questions/{question.id}/answers/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['text'] == answer.text
    
    def test_create_answer(self, api_client, question):
        response = api_client.post(
            f'/questions/{question.id}/answers/',
            {'user_id': 'user-123', 'text': 'Новый ответ'},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Answer.objects.filter(text='Новый ответ').exists()
    
    def test_create_answer_question_not_found(self, api_client, db):
        response = api_client.post(
            '/questions/999/answers/',
            {'user_id': 'user-123', 'text': 'Ответ'},
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_answer_with_empty_text(self, api_client, question):
        response = api_client.post(
            f'/questions/{question.id}/answers/',
            {'user_id': 'user-123', 'text': ''},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAnswerDetail:
    def test_get_answer(self, api_client, answer):
        response = api_client.get(f'/answers/{answer.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['text'] == answer.text
    
    def test_get_answer_not_found(self, api_client, db):
        response = api_client.get('/answers/999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_answer(self, api_client, answer):
        response = api_client.delete(f'/answers/{answer.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(id=answer.id).exists()
