from .views import (
    RegisterUserView,
    LogoutUserView,
    ChangePasswordView,
    UpdateUserview,
    UserDetailView,
)
from django.urls import path

urlpatterns = [
    path("detail/", UserDetailView.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("logout/", LogoutUserView.as_view()),
    path("change-password/<int:pk>/", ChangePasswordView.as_view()),
    path("update-user/<int:pk>/", UpdateUserview.as_view()),
]
