from django.urls import path
from .views import Perks, PerkDetail, ExperienceList

urlpatterns = [
    path("list/", ExperienceList.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
