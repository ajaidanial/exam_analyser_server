from rest_framework.viewsets import ModelViewSet

from exam_analyser.examination.models import Subject
from exam_analyser.examination.serializers import SubjectSerializer


class SubjectViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the Subject model."""

    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
