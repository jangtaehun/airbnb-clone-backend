from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer
from rest_framework import serializers
from rooms.serializer import RoomListSerializer


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
