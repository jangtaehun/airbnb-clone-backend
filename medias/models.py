from django.db import models
from common.models import CommonModel


class Photo(CommonModel):
    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        default="",
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        # 여러 사진을 함 개의 experience에 종속시킬 수 있다.
        "experiences.Experience",
        null=True,
        blank=True,
        default="",
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(self):
        return "Photo File"


# experience에만 종속된다.
class Viedo(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )  # ForeignKey와 비슷하지만 고유값이다. / 하나의 활동과 연결된다면 그 활동은 다른 영상을 가질 수 없다.

    def __str__(self):
        return "Video File"
