from django.shortcuts import render, get_object_or_404
from django.db.models import F  # Импортируем F
from .models import Building, TimeSlot, RoomUser, Room
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomUserLoginForm


def home(request):
    return render(request, 'index.html')


def buildings_list(request):
    buildings = Building.objects.all()
    return render(request, 'buildings_list.html', {'buildings': buildings})


def building_slots(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    rooms = building.room_set.all()
    return render(request, 'building_slots.html', {'building': building, 'rooms': rooms})


def room_slots(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    slots = TimeSlot.objects.filter(room=room, current_bookings__lt=F('max_bookings'))
    return render(request, 'room_slots.html', {'room': room, 'slots': slots})


@login_required
def book_slot(request):
    if request.method == 'POST':
        slot_id = request.POST.get('time_slot')
        slot = get_object_or_404(TimeSlot, id=slot_id)

        # Проверка, что пользователь уже забронировал этот слот
        existing_booking = RoomUser.objects.filter(user=request.user, time_slot=slot).exists()
        if existing_booking:
            return render(request, 'room_slots.html', {
                'room': slot.room,
                'slots': TimeSlot.objects.filter(room=slot.room, current_bookings__lt=F('max_bookings')),
                'error_message': "Вы уже забронировали этот слот."
            })

        if slot.current_bookings < slot.max_bookings:
            return render(request, 'payment.html', {'slot_id': slot.id})
        return render(request, 'room_slots.html', {
            'room': slot.room,
            'slots': TimeSlot.objects.filter(room=slot.room, current_bookings__lt=F('max_bookings')),
            'error_message': "Невозможно забронировать этот слот."
        })
    return HttpResponseBadRequest("Невозможно забронировать этот слот.")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматическая аутентификация и вход в систему после регистрации
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('buildings_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def auth_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Перенаправление на главную страницу после успешной авторизации
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Неверные учетные данные'})  # Возвращаем страницу входа с сообщением об ошибке
    else:
        form = CustomUserLoginForm()  # Создание формы для GET-запроса
    return render(request, 'login.html', {'form': form})  # Возвращаем страницу входа с формой для заполнения


@login_required
def auth_logout(request):
    logout(request)
    return redirect('/')  # После выхода из системы перенаправляем пользователя на страницу входа


@login_required
def profile(request):
    bookings = RoomUser.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(RoomUser, id=booking_id, user=request.user)
    slot = booking.time_slot
    booking.delete()
    slot.current_bookings = F('current_bookings') - 1
    slot.save()
    return redirect('profile')


@login_required
def payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        card_expiry_date = request.POST.get('card_expiry_date')
        card_cvv = request.POST.get('card_cvv')
        card_holder = request.POST.get('card_holder')
        slot_id = request.POST.get('slot_id')

        if card_number and card_expiry_date and card_cvv and card_holder:
            slot = get_object_or_404(TimeSlot, id=slot_id)
            RoomUser.objects.create(
                user=request.user,
                building=slot.room.building,
                time_slot=slot
            )
            slot.current_bookings = F('current_bookings') + 1
            slot.save()
            return redirect('/')
        else:
            return render(request, 'payment.html', {
                'error_message': "Оплата не прошла. Пожалуйста, заполните все поля.",
                'slot_id': slot_id
            })
    else:
        return HttpResponseBadRequest("Невозможно провести оплату.")