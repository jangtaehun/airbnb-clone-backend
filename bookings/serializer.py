from rest_framework import serializers
from .models import Booking
from django.utils import timezone


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Past!!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Past!!")
        return value

    def validate(self, data):
        if data["check_out"] < data["check_in"]:
            raise serializers.ValidationError("OMG!!")

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("이미 예약")
        return data


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.TimeField()
    experience_start = serializers.TimeField()
    experience_end = serializers.TimeField()
    check_in = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "experience",
            "check_in",
            "experience_time",
            "experience_start",
            "experience_end",
            "guests",
        )

    # def validate_experience_start(self, value):
    #     now = timezone.localtime(timezone.now()).time()
    #     if now > value:
    #         raise serializers.ValidationError("너무 늦었어!!")
    #     return value

    # def validate_experience_end(self, value):
    #     now = timezone.localtime(timezone.now()).time()
    #     if now > value:
    #         raise serializers.ValidationError("너무 늦었어!!")
    #     return value

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Past!!")
        return value

    def validate(self, date):
        if date["experience_start"] > date["experience_end"]:
            raise serializers.ValidationError("OMG!!")

        if date["experience_time"] < date["experience_start"]:
            raise serializers.ValidationError("너무 빨라")

        if date["experience_time"] > date["experience_end"]:
            raise serializers.ValidationError("너무 늦어")

        if Booking.objects.filter(check_in=date["check_in"]).exists():
            raise serializers.ValidationError("그날은 이미 예약")
        else:
            if Booking.objects.filter(
                experience_start__lte=date["experience_end"],
                experience_end__gte=date["experience_start"],
            ).exists():
                raise serializers.ValidationError("그 시간은 이미 예약")
        return date


class BookingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience",
            "check_in",
            "experience_time",
            "experience_start",
            "experience_end",
            "guests",
        )


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
