from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all pirces to zero")
def reset_prices(model_admin, request, a):  # rooms
    print(model_admin)
    print(request)
    print(a)
    for room in a.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    # 기본적으로 Django는 포함하는 것들을 찾아준다. -> __contains__
    search_fields = (
        # "name",
        # "=price",
        "owner__username",
    )

    # def total_amenities(self, room):
    #     return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
