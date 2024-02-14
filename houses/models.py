from django.db import models
from django.conf import settings


# Create your models here.
class House(models.Model):
    """sumary_line
    Model Definition for House
    """

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(
        verbose_name="Pets Allowed?",
        default=True,
        help_text="Does this house allow pet?",
    )
    ower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 참조하는 모델이 삭제될 때 어떻게 할 것인지 설정 / models.SET_NULL: 삭제돼도 유지
    )

    def __str__(self):
        return self.name
