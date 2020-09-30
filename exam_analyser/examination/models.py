from django.db import models


class Subject(models.Model):
    """
    Model that holds the subject name data. This is linked to the teacher and the student
    and is used in mapping the exams dynamically.
    """

    name = models.CharField(max_length=255)
