from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'file', 'content', 'is_indexed', 'created_at', 'updated_at')
        read_only_fields = ('content', 'is_indexed', 'created_at', 'updated_at')


