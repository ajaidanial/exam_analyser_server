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
