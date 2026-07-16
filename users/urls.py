from django.urls import path

from users.views import CreateUserView, DetailUserView

urlpatterns = [
    path("", CreateUserView.as_view()),
    path("<int:pk>/", DetailUserView.as_view(), name="user-detail"),
]
