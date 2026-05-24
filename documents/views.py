from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rag.indexer import index_document, delete_document_index


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()
        try:
            index_document(document)
        except Exception as e:
            print(f"Indexing error: {e}")

    def perform_update(self, serializer):
        document = serializer.save()
        try:
            delete_document_index(document.id)
            index_document(document)
        except Exception as e:
            print(f"Re-indexing error: {e}")

    def perform_destroy(self, instance):
        try:
            delete_document_index(instance.id)
        except Exception as e:
            print(f"Delete index error: {e}")
        instance.delete()

    @action(detail=True, methods=['post'])
    def reindex(self, request, pk=None):
        document = self.get_object()
        try:
            delete_document_index(document.id)
            index_document(document)
            return Response({'status': 'reindexed successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
