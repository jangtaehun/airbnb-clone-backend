from django.db import models
from common.models import CommonModel
from django.conf import settings


class Wishlist(CommonModel):
    """Wishlist Model Dfinition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
    )
    experiences = models.ManyToManyField(
        "experiences.Experience",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
