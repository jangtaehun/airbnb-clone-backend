from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers

# from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


# 자동으로 id, created_at은 read_only인 property로 되어있다.


class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
        # depth = 1  # 모델의 모든 관계 확장 / 커스터마이즈 할 수 없다.


class RoomDetailSerializer(ModelSerializer):

    # 역접근자
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )  # manytomany -> list형태로 전달
    category = CategorySerializer(read_only=True)
    # Django REST Framework 또는 Django가 owner를 serializer하려 하면 TinyUserSerializer를 사용하라고 알려준다.

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    photos = PhotoSerializer(many=True, read_only=True)
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        model = Room
        fields = "__all__"

    # get_ + 계산하려는 속성의 이름을 붙여야 한다.
    # 현재 serializing하고 있는 오브젝트와 함께 호출
    def get_rating(self, room):
        print("\n")
        print(self.context)
        print(room.rating())
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    # room => serializer에서 serializer하는 것
    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(user=request.user, rooms__pk=room.pk).exists()

    # def create(self, validated_data):
    #     print(validated_data)
    #     return

    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)
    # serializer.save(owner=request.user)을 호출하면
    # owner=request.user가 validated_data에 자동으로 추가된다.
    # 굳이 정의할 필요 없이 serializer.save(owner=request.user)만 해주면 된다.
