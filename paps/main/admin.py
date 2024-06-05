from django.contrib import admin
from .models import Building, Room, TimeSlot, RoomUser


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'image', 'description')
    list_display_links = ('id', 'address')
    search_fields = ('address', 'description')
    list_filter = ('address',)
    fieldsets = (
        (None, {
            'fields': ('address', 'image', 'description')
        }),
    )
    search_help_text = 'Введите адресс'



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'free_places_counter', 'image', 'description')
    list_display_links = ('id', 'building')
    search_fields = ('building__address', 'description')
    list_filter = ('building',)
    fieldsets = (
        (None, {
            'fields': ('building', 'free_places_counter', 'image', 'description')
        }),
    )
    search_help_text = 'Введите адресс здания'



@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'start_time', 'end_time', 'max_bookings', 'current_bookings')
    list_display_links = ('id', 'room')
    search_fields = ('room__building__address',)
    list_filter = ('room__building', 'start_time', 'end_time')
    fieldsets = (
        (None, {
            'fields': ('room', 'start_time', 'end_time', 'max_bookings', 'current_bookings')
        }),
    )
    search_help_text = 'Введите номер комнаты или адресс здания'



@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'building', 'time_slot')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'building__address', 'time_slot__room__building__address')
    list_filter = ('building', 'time_slot__room__building')
    fieldsets = (
        (None, {
            'fields': ('user', 'building', 'time_slot')
        }),
    )
    search_help_text = 'Введите номер комнаты, адресс здания или временной слот'


