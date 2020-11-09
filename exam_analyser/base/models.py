import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class BaseModel(TimeStampedModel, models.Model):
    """Base model class for all the models used in the application. Contains common method."""

    class Meta:
        abstract = True
        ordering = ["created"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        """Returns the display name to the admin panel, based on the defined priority."""

        # 0th index will have more priority
        AVAILABLE_DISPLAY_NAMES = ["username", "name", "id"]

        for _ in AVAILABLE_DISPLAY_NAMES:
            if hasattr(self, _):
                return str(getattr(self, _))
