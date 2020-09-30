from rest_framework.serializers import ModelSerializer

from exam_analyser.examination.models import Subject, Exam, QuestionCategory


class SubjectSerializer(ModelSerializer):
    """Serializer to handle CRUD operations for the subject model."""

    class Meta:
        model = Subject
        fields = ["id", "name"]


class ExamSerializer(ModelSerializer):
    """Serializer to handle CRUD operations for the Exam model."""

    class Meta:
        model = Exam
        fields = ["id", "name"]


class QuestionCategorySerializer(ModelSerializer):
    """Serializer to handle CRUD operations for the QuestionCategory model."""

    class Meta:
        model = QuestionCategory
        fields = ["id", "name"]
