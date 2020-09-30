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
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)

        # password should be passed on create | user will be created without hashing password
        user.set_password(validated_data["password"])

        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)

        # password may or may not be passed while update | if passed | hash and save it
        if "password" in validated_data.keys():
            user.set_password(validated_data["password"])

        return user

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)

        data["linked_subjects"] = SubjectSerializer(
            instance.linked_subjects.all(), context=self.context, many=True
        ).data

        return data
