from django.urls import path
from .views import login_view, health_check

urlpatterns = [
    path("login/", login_view, name="login"),
]