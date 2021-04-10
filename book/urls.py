from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index.as_view()),
    path('room', views.room.as_view()),
    path('room_type', views.room_type.as_view()),
    path('record', views.booking_record.as_view()),
    path('money', views.money.as_view()),

]