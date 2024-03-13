import jwt
import requests

from django.conf import settings
from django.contrib.auth import login, authenticate, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound

from .models import User
from reviews.models import Reviews
from reviews.serializers import ReviewSerializer
from rooms.models import Room
from rooms.serializer import RoomListSerializer

from .serializer import PrivateUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            new_user = serializer.save()
            serializer = PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class UserReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username):
        all_reviews = Reviews.objects.filter(user__username=username)
        print(all_reviews)
        serializer = ReviewSerializer(
            all_reviews,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


# __ 은 관계를 나타내는 Django ORN,
# Reviews.objects.filter(user__username=username) -> Reviews 모델에서 user가 username인 것에 접근


class UserRoom(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username):
        all_rooms = Room.objects.filter(owner__username=username)
        print(all_rooms)
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


# context={"request": request}
# Serializer의 context에 'request' 키가 없기 때문에 발생 -> request 객체를 serializer로 전달하지 않았을 때 발생
# View에서 Serializer를 사용할 때 context에 request 객체를 넣어서 Serializer에 전달하는 것이 일반적
# 왜?  여러 개의 객체가 포함된 QuerySet => <QuerySet [<Room: 뭉치네>, <Room: 루루네>, <Room: zzone House>]>
# 쿼리셋이 여러 개의 객체를 반환하는 경우에는 context={'request': request}와 같이 request 객체를 전달하는 것을 권장


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"ok": "Welcom!"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})


class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogin(APIView):

    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=a39903303d8e1aadf8f5&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            print(user_data)

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            print(user_emails)
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name") if user_data.get("name") else "No Name",
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()  # 이 유저는 password로 로근인을 할 수 없기 때문에 설정 / .has_usable_password
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "2a7311e4d93424f2afe213fdd938125b",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            print(access_token.json(), "\n")

            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            print(user_data, "\n")

            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            print(profile)
            try:
                user = User.objects.get(username=profile.get("nickname"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()  # 이 유저는 password로 로근인을 할 수 없기 때문에 설정 / .has_usable_password
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
