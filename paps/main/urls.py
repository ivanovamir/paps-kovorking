from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buildings/', views.buildings_list, name='buildings_list'),
    path('<int:building_id>/slots/', views.building_slots, name='building_slots'),
    path('room/<int:room_id>/slots/', views.room_slots, name='room_slots'),
    path('book_slot/', views.book_slot, name='book_slot'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('login/', views.auth_login, name='auth_login'),
    path('profile/', views.profile, name='profile'),
    path('payment/', views.payment, name='payment'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
