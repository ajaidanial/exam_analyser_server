from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField

from exam_analyser.base.models import BaseModel
from exam_analyser.configurations import ROLES


class User(BaseModel, AbstractUser):
    """
    User model for the entire application. This is used to denote the following user types:
        1. Admin (super user)
        2. Teacher (can add students and other question paper stuff)
        3. Student (cannot do anything | cannot even login)
    The above permissions are denoted by the `self.role` field. Also contains
    other data and methods related to the application.
    """

    class Meta:
        default_related_name = "related_users"

    ROLE_CHOICES = Choices(*ROLES["options"])

    role = StatusField(choices_name="ROLE_CHOICES", default=ROLES["default_option"])
    linked_subjects = models.ManyToManyField(to="examination.Subject")

    def set_password(self, raw_password):
        """Hashed the input raw password and saves it to the user instance."""

        self.password = make_password(raw_password)
        self._password = raw_password
        self.save()
