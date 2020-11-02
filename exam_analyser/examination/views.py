from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from exam_analyser.examination.models import (
    Subject,
    Exam,
    QuestionCategory,
    QuestionPaper,
    Question,
)
from exam_analyser.examination.serializers import (
    SubjectSerializer,
    ExamSerializer,
    QuestionCategorySerializer,
    QuestionPaperSerializer,
    QuestionSerializer,
)


class SubjectViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the Subject model."""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class ExamViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the Exam model."""

    serializer_class = ExamSerializer
    queryset = Exam.objects.all()


class QuestionCategoryViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the QuestionCategory model."""

    serializer_class = QuestionCategorySerializer
    queryset = QuestionCategory.objects.all()


class QuestionPaperViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the QuestionPaper model."""

    serializer_class = QuestionPaperSerializer
    queryset = QuestionPaper.objects.all()


class QuestionViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the Question model."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class ExamSubjectOverviewView(APIView):
    """
    This view displays the data for the exam, subject and question paper view.
    This gives the data for the table like view through which the question paper can be viewed
    or created. This will include the exam, subject and question paper.
    """

    def get(self, request, **kwargs):
        overview_data = {}
        return Response(data=overview_data, status=status.HTTP_200_OK)
