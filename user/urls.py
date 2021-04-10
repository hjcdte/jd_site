from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login.as_view()),
    path('register', views.register),
    path('staff', views.staff.as_view()),
    path('jwt', views.jwt.as_view())

]