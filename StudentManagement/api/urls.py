from django.urls import path, include
from . import views

urlpatterns = [
    path("login_view", views.login_view, name="login_view"),
    ]