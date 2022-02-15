from .views import RegisterUserView
from django.urls import path

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
]