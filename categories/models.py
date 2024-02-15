from django.db import models
from django.conf import settings
from common.models import CommonModel


class Category(CommonModel):
    """Room and Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOM = (
            "room",
            "Room",
        )
        EXPERIENCES = (
            "experiences",
            "Experiences",
        )

    name = models.CharField(
        max_length=50,
    )
    kind = models.CharField(
        max_length=20,
        choices=CategoryKindChoices.choices,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.kind.title()}: {self.name}"
