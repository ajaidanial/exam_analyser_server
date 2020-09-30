from rest_framework.serializers import ModelSerializer

from exam_analyser.examination.models import Subject


class SubjectSerializer(ModelSerializer):
    """Serializer to handle CRUD operations for the subject model."""

    class Meta:
        model = Subject
        fields = ["id", "name"]
