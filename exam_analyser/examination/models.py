from django.db import models

from exam_analyser.base.models import BaseModel


class Subject(BaseModel):
    """
    Model that holds the subject name data. This is linked to the teacher and the student
    and is used in mapping the exams dynamically.
    """

    name = models.CharField(max_length=255, unique=True)


class Exam(BaseModel):
    """
    Model that holds the exam name data. This is linked to the question papers. This is mostly
    a read only data for now. This contains the values:
        1. Quarterly Exam
        2. Half Yearly Exam
        3. Annual Exam
    This might get dynamic in the future.
    """

    name = models.CharField(max_length=255, unique=True)


class QuestionCategory(BaseModel):
    """Model that holds the question category data. This is used while creating questions."""

    name = models.CharField(max_length=255, unique=True)
    subject = models.ForeignKey(to="examination.Subject", on_delete=models.CASCADE)


class QuestionPaper(BaseModel):
    """
    Model that holds the QuestionPaper data under a given exam and a subject.
    This is unique under tha same. There are questions linked under the question paper.
    """

    class Meta(BaseModel.Meta):
        unique_together = ("exam", "subject")
        default_related_name = "related_question_papers"

    name = models.TextField()
    description = models.TextField()
    exam = models.ForeignKey(to="examination.Exam", on_delete=models.CASCADE)
    subject = models.ForeignKey(to="examination.Subject", on_delete=models.CASCADE)


class Question(BaseModel):
    """Model that holds the Question data under a given question paper."""

    class Meta(BaseModel.Meta):
        unique_together = ("name", "question_paper")
        default_related_name = "related_questions"

    name = models.TextField()
    description = models.TextField(null=True, default=None)
    question_categories = models.ManyToManyField(to="examination.QuestionCategory")
    question_paper = models.ForeignKey(
        to="examination.QuestionPaper", on_delete=models.CASCADE
    )
    max_marks = models.PositiveIntegerField()


class UserQuestionMarkTracker(BaseModel):
    """
    This model keeps track of the mark obtained by the user for a given question.
    This is created from the UploadMarkView.
    """

    class Meta(BaseModel.Meta):
        unique_together = ("user", "question")
        default_related_name = "related_mark_trackers"
        ordering = ["user", "-question"]

    user = models.ForeignKey(to="authentication.User", on_delete=models.CASCADE)
    question = models.ForeignKey(to="examination.Question", on_delete=models.CASCADE)
    mark = models.PositiveIntegerField(null=True)
