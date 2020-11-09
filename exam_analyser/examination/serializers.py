from rest_framework import serializers

from exam_analyser.examination.models import (
    Subject,
    Exam,
    QuestionCategory,
    QuestionPaper,
    Question,
)


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer to handle CRUD operations for the subject model."""

    class Meta:
        model = Subject
        fields = ["id", "name"]


class ExamSerializer(serializers.ModelSerializer):
    """Serializer to handle CRUD operations for the Exam model."""

    class Meta:
        model = Exam
        fields = ["id", "name"]


class QuestionCategorySerializer(serializers.ModelSerializer):
    """Serializer to handle CRUD operations for the QuestionCategory model."""

    class Meta:
        model = QuestionCategory
        fields = ["id", "name", "subject"]


class QuestionPaperSerializer(serializers.ModelSerializer):
    """Serializer to handle CRUD operations for the QuestionPaper model."""

    class Meta:
        model = QuestionPaper
        fields = ["id", "name", "description", "exam", "subject"]

    def to_representation(self, instance):
        data = super(QuestionPaperSerializer, self).to_representation(instance)

        request = self.context["request"]
        if request.query_params.get("show-questions", False):
            data["related_questions"] = QuestionSerializer(
                instance.related_questions.all(), context=self.context, many=True
            ).data

        return data


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer to handle CRUD operations for the Question model."""

    class Meta:
        model = Question
        fields = [
            "id",
            "name",
            "description",
            "question_categories",
            "question_paper",
            "max_marks",
        ]


class MarksUploadSerializer(serializers.Serializer):
    """Serializer to handle the input file for the QuestionPaperMarksUploadView on POST."""

    file = serializers.FileField()

    class Meta:
        fields = ["file"]
