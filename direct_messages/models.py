from django.db import models
from common.models import CommonModel
from django.conf import settings


class Message(CommonModel):
    """Room Model Definition"""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
