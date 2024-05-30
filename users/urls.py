from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.user_register,name='user_register'),
    #path('register/',views.signup,name='user_register'),

    path('login/',views.user_login,name='users_login'),
    path('logout/',views.user_logout,name='users_logout'),
    path('profile/',views.user_profile,name='user_profile'),



]
