from django.db import models


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField('Текст вопроса')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

        
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        verbose_name='ID вопроса',
        related_name='answers'
    )
    user_id = models.CharField(max_length=255, verbose_name='Идентификатор пользователя')
    text = models.TextField('Текст ответа')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'