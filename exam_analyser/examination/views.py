from typing import Union

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from exam_analyser.authentication.models import User
from exam_analyser.base.views import CheckParamsMixin
from exam_analyser.examination.helpers import (
    write_data_to_excel_and_get_public_url,
    get_data_as_list_of_dict_from_excel_file,
)
from exam_analyser.examination.models import (
    Subject,
    Exam,
    QuestionCategory,
    QuestionPaper,
    Question,
    UserQuestionMarkTracker,
)
from exam_analyser.examination.serializers import (
    SubjectSerializer,
    ExamSerializer,
    QuestionCategorySerializer,
    QuestionPaperSerializer,
    QuestionSerializer,
    MarksUploadSerializer,
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


class DashboardDataAPIView(APIView):
    """Returns the data necessary for the users dashboard cards."""

    def get(self, request, **kwargs):
        output_data = [
            {"display_name": "Subjects Count", "value": Subject.objects.all().count()},
            {
                "display_name": "Teachers Count",
                "value": User.objects.filter(role="teacher").count(),
            },
            {
                "display_name": "Students Count",
                "value": User.objects.filter(role="student").count(),
            },
            {"display_name": "Exams Count", "value": Exam.objects.all().count()},
            {
                "display_name": "Question Papers Count",
                "value": QuestionPaper.objects.all().count(),
            },
            {
                "display_name": "Categories Count",
                "value": QuestionCategory.objects.all().count(),
            },
        ]
        return Response(data=output_data)


class QuestionPaperMarksUploadView(CheckParamsMixin, APIView):
    """
    This view does two things:
        1. Updates the students marks under a given question paper and a question on POST request
        2. On get request, returns the upload help file for the POST request.
    """

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, **kwargs):
        """On get, returns the upload help file used for the post request."""

        self.init_params_for_view(request)
        question_paper = QuestionPaper.objects.get(
            id=request.query_params.get("question_paper_id")
        )
        questions = question_paper.related_questions.all()
        students = User.objects.filter(role="student")
        data_to_write_in_excel = []

        for student in students:
            student_data = {"username": student.username}

            for question_index in range(0, len(questions)):
                student_data[f"Q.NO {question_index + 1}"] = ""

            data_to_write_in_excel.append(student_data)

        public_url = write_data_to_excel_and_get_public_url(
            data_to_write_in_excel, request
        )
        return Response(data={"url": public_url})

    def post(self, request, **kwargs):
        """On post, updates the students marks under each question."""

        self.init_params_for_view(request)

        serializer = MarksUploadSerializer(
            data=request.data, context={"view": self, "request": request}
        )
        serializer.is_valid(raise_exception=True)

        file_data = get_data_as_list_of_dict_from_excel_file(
            excel_file_config={
                "file_contents": serializer.validated_data["file"].read()
            },
            input_indexes_and_dict_keys={
                0: "username",
            },
            read_other_excel_data=True,
        )

        question_paper = QuestionPaper.objects.get(
            id=request.query_params.get("question_paper_id")
        )
        questions = question_paper.related_questions.all()

        for data in file_data:
            user = User.objects.get(username=data["username"])
            UserQuestionMarkTracker.objects.filter(
                user=user, question__in=questions
            ).delete()

            marks_obtained: list = data["other_excel_data"]

            for question_index in range(0, len(questions)):
                question = questions[question_index]
                mark: Union[None, int] = marks_obtained[question_index]
                UserQuestionMarkTracker.objects.create(
                    user=user, question=question, mark=mark
                )

        return Response(data=None)

    def init_params_for_view(self, request):
        """Checks the necessary params and returns a tuple (is_success, error_response)"""

        self.query_params_dict = {
            "question_paper_id": list(
                QuestionPaper.objects.values_list("id", flat=True)
            )
        }
        self.check_params(request)
