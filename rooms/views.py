from django.db import transaction
from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializer import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from .models import Amenity, Room
from categories.models import Category
from bookings.models import Booking
from bookings.serializer import PublicBookingSerializer, CreateRoomBookingSerializer


# transaction 모든 변경사항을 원래 상태로 되돌려 놓는다


# /api/v1/rooms/amenities
class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            new_amenities = serializer.save()
            return Response(AmenitySerializer(new_amenities).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# /api/v1/rooms/amenities/1
class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amentity = self.get_object(pk)
        serializer = AmenitySerializer(amentity)
        return Response(serializer.data)

    def put(self, request, pk):
        amentity = self.get_object(pk)
        serializer = AmenitySerializer(
            amentity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            update_amenity = serializer.save()
            return Response(AmenitySerializer(update_amenity).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class AmenitiseView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_room = Room.objects.all()
        serializer = RoomListSerializer(
            all_room,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        # print(dir(request.user))
        # if request.user.is_authenticated:  # 인증받지 않은 사용자 오류 / IsAuthenticatedOrReadOnly 사용으로 생략 가능
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():

            # category 추가
            category_pk = request.data.get("category")
            print(request.data)  # 유저가 입력한 값이 딕셔너리 형태로 전달된다.
            print(category_pk)  # key가 category인 것을 선택
            print(request.user)
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    new_room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    # 누가 room의 owner인지 알려준다. 자동으로 owner를 방에 추가해준다. / models에 owner로 정의되어 있어서 owner!!
                    # 이 지점에서 ownerdhk category와 함께 방을 생성하고 있다.

                    # amenit 추가
                    # request data에 amenities가 존재하면 개별의 amenity들을 찾아서 방에 추가한다.
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)

                        # manytomany는 add()를 통해 추가시켜야 한다. / remove()
                        new_room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(new_room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Ameniti not found")

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # else:
    #     raise NotAuthenticated


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room, context={"request": request}  # 원하는 시리얼라이저에 전달할 수 있다.
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        # 방의 주인이 아니면 수정할 수 없다.
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_room = serializer.save()
            return Response(RoomDetailSerializer(updated_room).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        # 방의 주인이 아니면 삭제할 수 없다.
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # print(request.query_params)
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        print(room)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(  # serializer에 추가적인 데이터 보내기
                user=request.user,
                room=self.get_object(
                    pk,
                ),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.in_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.now().date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gte=now,
        )
        PhotoSerializer = PublicBookingSerializer(bookings, many=True)
        return Response(PhotoSerializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
