from django.urls import path
from .views import Me, Users, PublicUser, ChangePassword, UserReviews, UserRoom


urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("@<str:username>", PublicUser.as_view()),
    path("@<str:username>/reviews", UserReviews.as_view()),
    path("@<str:username>/rooms", UserRoom.as_view()),
]
