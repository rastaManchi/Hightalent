import logging
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, QuestionDetailSerializer

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def question_list(request: Request) -> Response:
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            logger.info(f"Создан вопрос id={question.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Ошибка валидации при создании вопроса: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def question_detail(request: Request, id: int) -> Response:
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        logger.warning(f"Вопрос id={id} не найден")
        return Response({'error': 'Вопрос не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        question.delete()
        logger.info(f"Удален вопрос id={id} вместе с ответами")
        return Response({'text': 'Вопрос удален вместе со всеми ответами.'}, status=status.HTTP_204_NO_CONTENT)
    
    serializer = QuestionDetailSerializer(question)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def answer_list(request: Request, id: int) -> Response:
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        logger.warning(f"Попытка работы с ответами несуществующего вопроса id={id}")
        return Response({'error': 'Вопрос не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        data = request.data.copy()
        data['question_id'] = id
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            answer = serializer.save()
            logger.info(f"Создан ответ id={answer.id} на вопрос id={id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Ошибка валидации при создании ответа: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    answers = Answer.objects.filter(question_id=question)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def answer_detail(request: Request, id: int) -> Response:
    try:
        answer = Answer.objects.get(id=id)
    except Answer.DoesNotExist:
        logger.warning(f"Ответ id={id} не найден")
        return Response({'error': 'Ответ не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        answer.delete()
        logger.info(f"Удален ответ id={id}")
        return Response({'text': 'Ответ удален.'}, status=status.HTTP_204_NO_CONTENT)
    
    serializer = AnswerSerializer(answer)
    return Response(serializer.data)