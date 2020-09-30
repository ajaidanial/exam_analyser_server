from rest_framework.serializers import ModelSerializer

from exam_analyser.authentication.models import User


class UserSerializer(ModelSerializer):
    """Serializer for the user model. Handles the data for all the CRUD operations."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        ]
