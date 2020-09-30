from rest_framework import serializers

from exam_analyser.authentication.models import User
from exam_analyser.examination.serializers import SubjectSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model. Handles the data for all the CRUD operations."""

    confirm_password = serializers.CharField(allow_null=True)

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
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_confirm_password(self, value):
        if "password" in self.initial_data.keys():
            if self.initial_data["password"] != value:
                raise serializers.ValidationError(
                    "Password and confirm password does not seem to match."
                )
        return None

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        user = super(UserSerializer, self).create(validated_data)

        # password should be passed on create | user will be created without hashing password
        user.set_password(validated_data["password"])

        return user

    def update(self, instance, validated_data):
        validated_data.pop("confirm_password", None)
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
