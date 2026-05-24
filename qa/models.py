from django.db import models


class Question(models.Model):
    question_text = models.TextField(verbose_name='پرسش')
    answer_text = models.TextField(blank=True, verbose_name='پاسخ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پرسش'
        verbose_name_plural = 'پرسش‌ها'
        ordering = ('-created_at',)

    def __str__(self):
        return self.question_text[:80]


class QuestionSource(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='sources'
    )
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.SET_NULL,
        null=True
    )
    relevant_chunk = models.TextField(verbose_name='بخش مرتبط')

    class Meta:
        verbose_name = 'منبع'
        verbose_name_plural = 'منابع'


