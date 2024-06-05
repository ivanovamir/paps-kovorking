from django.contrib import admin
from .models import Building, Room, TimeSlot, RoomUser

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(TimeSlot)
admin.site.register(RoomUser)