from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    address = models.TextField(verbose_name=_("Адрес"))
    image = models.ImageField(upload_to='building_images/', default='test', verbose_name=_("Изображение"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Здание")
        verbose_name_plural = _("Здания")

    def __str__(self):
        return f"Здание {self.address}"


class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_("Здание"))
    free_places_counter = models.BigIntegerField(verbose_name=_("Количество свободных мест"))
    image = models.ImageField(upload_to='room_images/', default='test', verbose_name=_("Изображение"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))

    class Meta:
        verbose_name = _("Помещение")
        verbose_name_plural = _("Помещения")

    def __str__(self):
        return f"Помещение {self.id} in {self.building}"


class TimeSlot(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("Помещение"))
    start_time = models.DateTimeField(verbose_name=_("Начальное время"))
    end_time = models.DateTimeField(verbose_name=_("Конечное время"))
    max_bookings = models.IntegerField(verbose_name=_("Максимальное количество бронирований"))
    current_bookings = models.IntegerField(default=0, verbose_name=_("Текущее количество бронирований"))

    class Meta:
        verbose_name = _("Временной интервал")
        verbose_name_plural = _("Временные интервалы")

    def __str__(self):
        return f"Время {self.id} for {self.room}"


class RoomUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_("Здание"))
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, verbose_name=_("Временной интервал"))

    class Meta:
        verbose_name = _("Пользователь помещения")
        verbose_name_plural = _("Пользователи помещений")

    def __str__(self):
        return f"{self.user} забронировал {self.time_slot}"
