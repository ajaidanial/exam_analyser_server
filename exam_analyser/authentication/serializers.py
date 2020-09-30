from rest_framework.serializers import ModelSerializer

from exam_analyser.authentication.models import User
from exam_analyser.examination.serializers import SubjectSerializer


class UserSerializer(ModelSerializer):
    """Serializer for the user model. Handles the data for all the CRUD operations."""

    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "linked_subjects",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)

        data["linked_subjects"] = SubjectSerializer(
            instance.linked_subjects.all(), context=self.context, many=True
        ).data

        return data
