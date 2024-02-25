from django.urls import path
from .views import (
    Perks,
    PerkDetail,
    ExperienceList,
    ExperienceDetail,
    ExperiencePerk,
    ExperienceBooking,
    ExperienceDelete,
)

urlpatterns = [
    path("", ExperienceList.as_view()),
    path("<int:pk>", ExperienceDetail.as_view()),
    path("<int:pk>/perks", ExperiencePerk.as_view()),
    path("<int:pk>/bookings", ExperienceBooking.as_view()),
    path("<int:pk>/bookings/<int:ex_pk>", ExperienceDelete.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]
