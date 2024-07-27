from django.contrib import admin
from django.urls import path
from .app.views import (
    RegisterUser,
    LoginUser,
    LogoutUser,
    UserAuthentication
)

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogoutUser.as_view(), name="logout"),
    path('check_user/', UserAuthentication.as_view(), name="check_user"),
]