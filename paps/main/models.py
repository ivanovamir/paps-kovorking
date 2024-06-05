from django.db import models
from django.conf import settings

class Building(models.Model):
    address = models.TextField()
    image = models.ImageField(upload_to='building_images/', default='test')
    description = models.TextField(blank=True)  # Добавляем поле описания

    def __str__(self):
        return f"Здание {self.address}"

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    free_places_counter = models.BigIntegerField()
    image = models.ImageField(upload_to='room_images/', default='test')
    description = models.TextField(blank=True)  # Добавляем поле описания

    def __str__(self):
        return f"Помещение {self.id} in {self.building}"

class TimeSlot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_bookings = models.IntegerField()
    current_bookings = models.IntegerField(default=0)

    def __str__(self):
        return f"Время {self.id} for {self.room}"

class RoomUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} забронировано {self.time_slot}"
