from django.contrib import admin
from .models import Reviews


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Greate"),
            ("awesome", "Awesom"),
        ]

    def queryset(self, request, reviews):
        # self.value() => url에 있는 읽어서 준다.
        word = self.value()
        if word is None:
            pass
        else:
            return reviews.filter(
                payload__contains=word,
            )


class ScoreFilter(admin.SimpleListFilter):
    title = "평점으로 보기"
    parameter_name = "scroe"

    def lookups(self, request, model_admin):  # 튜플의 리스트를 리턴해야 한다.
        return [
            ("3", "Middle"),
            ("4", "Hight"),
            ("5", "Recomment"),
        ]

    def queryset(self, request, rating):
        print(rating)
        rate = self.value()
        if rate is None:
            pass
        else:
            return rating.filter(
                rating__contains=rate,
            )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",  # models.py 에서 설정한 str 메서드를 보여준다.
        "payload",
    )
    list_filter = (
        WordFilter,
        ScoreFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
