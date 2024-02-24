from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Perk, Experience


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        exclude = ("created_at", "updated_at")


class ExperienceSerializer(ModelSerializer):

    class Meta:
        model = Experience
        fields = "__all__"


class ExperiencePerkSerializer(ModelSerializer):
    # perks = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = ("perks",)

    # def get_perks(self, experience):
