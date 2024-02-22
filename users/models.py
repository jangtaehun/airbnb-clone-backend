from django.db import models
from django.contrib.auth.models import AbstractUser


# user을 조작할 수 있는 class
class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = (
            "male",
            "Male",
        )  # database에 들어갈 value, 관리자 페이지에서 보게 될 label이 들어간다.
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = (
            "won",
            "korean won",
        )
        USD = (
            "usd",
            "Dolar",
        )

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.URLField(blank=True)  # form에서 필드가 필수적이지 않게 해준다.
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices)
    # 각 Choices 안에 있는 TextChoices 가리키기 때문에 .choices
