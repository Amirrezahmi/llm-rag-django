from rest_framework import serializers
from .models import Question, QuestionSource


class QuestionSourceSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(
        source='document.title',
        read_only=True
    )

    class Meta:
        model = QuestionSource
        fields = ('document_title', 'relevant_chunk')


class QuestionSerializer(serializers.ModelSerializer):
    sources = QuestionSourceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'answer_text', 'sources', 'created_at')
        read_only_fields = ('answer_text', 'sources', 'created_at')
