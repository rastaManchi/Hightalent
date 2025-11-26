from rest_framework import serializers
from .models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'Текст вопроса не может быть пустым'}
    )
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class AnswerSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'Текст ответа не может быть пустым'}
    )
    user_id = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'ID пользователя не может быть пустым'}
    )
    
    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']
        read_only_fields = ['created_at']

