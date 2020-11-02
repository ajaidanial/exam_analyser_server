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

    Output Schema: [
        {
            ...
            "linked_subjects": [
                {
                    ...
                    "linked_question_paper": {} || null
                }
                ... subjects data
            ]
        }
        ...exams data
    ]
    """

    def get(self, request, **kwargs):
        overview_data = ExamSerializer(
            Exam.objects.all(), context=self.get_serializer_context(), many=True
        ).data

        for exam_data in overview_data:
            exam_id = exam_data["id"]
            exam_data["linked_subjects"] = SubjectSerializer(
                Subject.objects.all(), context=self.get_serializer_context(), many=True
            ).data
            for subject_data in exam_data["linked_subjects"]:
                subject_id = subject_data["id"]
                question_paper_qs = QuestionPaper.objects.filter(
                    exam=exam_id, subject=subject_id
                )
                subject_data["linked_question_paper"] = (
                    QuestionPaperSerializer(
                        question_paper_qs.first(), context=self.get_serializer_context()
                    ).data
                    if question_paper_qs.exists()
                    else None
                )

        return Response(data=overview_data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {"view": self, "request": self.request}
