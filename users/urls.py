from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import (
    Me,
    Users,
    PublicUser,
    ChangePassword,
    UserReviews,
    UserRoom,
    LogIn,
    LogOut,
)


urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("change-password", ChangePassword.as_view()),
    path("@<str:username>", PublicUser.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
    path("@<str:username>/reviews", UserReviews.as_view()),
    path("@<str:username>/rooms", UserRoom.as_view()),
    path("token-login", obtain_auth_token),
    path("github", views.GithubLogin.as_view()),
    path("kakao", views.KakaoLogin.as_view()),
    path("jwt-login", views.JWTLogIn.as_view()),
]
