from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Question, QuestionSource
from .serializers import QuestionSerializer
from rag.chain import get_answer


class QuestionViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_text = serializer.validated_data['question_text']

        try:
            result = get_answer(question_text)
            question = Question.objects.create(
                question_text=question_text,
                answer_text=result['answer']
            )
            for source in result.get('sources', []):
                QuestionSource.objects.create(
                    question=question,
                    document=source.get('document'),
                    relevant_chunk=source.get('chunk', '')
                )
            return Response(
                QuestionSerializer(question).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


