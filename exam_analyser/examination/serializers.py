from rest_framework import serializers

from exam_analyser.authentication.models import User
from exam_analyser.examination.models import (
    Subject,
    Exam,
    QuestionCategory,
    QuestionPaper,
    Question,
    UserQuestionMarkTracker,
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

        if request.query_params.get("show-user-report", False):
            entire_trackers = UserQuestionMarkTracker.objects.filter(
                question__in=instance.related_questions.all()
            )
            users = User.objects.filter(role="student")
            entire_users_report = []

            for user in users:
                user_trackers = entire_trackers.filter(user=user)
                single_user_report = {"name": user.username}

                for tracker_index in range(0, len(user_trackers)):
                    single_user_report[tracker_index] = user_trackers[
                        tracker_index
                    ].mark

                entire_users_report.append(single_user_report)

            data["users_report"] = entire_users_report

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
