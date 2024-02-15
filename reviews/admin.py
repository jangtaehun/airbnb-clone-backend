from django.contrib import admin
from .models import Reviews


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",  # models.py 에서 설정한 str 메서드를 보여준다.
        "payload",
    )
    list_filter = ("rating",)
