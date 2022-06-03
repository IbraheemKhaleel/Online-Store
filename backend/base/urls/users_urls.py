from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import TokenObtainPairView

from base.views import users_views as views

urlpatterns = [
    path('register/', views.userRegistration, name='register'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('details/', views.GetAllUsers, name='user-details'),
]