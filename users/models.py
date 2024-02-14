from django.db import models
from django.contrib.auth.models import AbstractUser


# user을 조작할 수 있는 class
class User(AbstractUser):
    pass
