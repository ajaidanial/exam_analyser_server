from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "authentication"

router = SimpleRouter()
router.register("users", views.UserViewSet, basename="user_viewset")

urlpatterns = [
    path("get-auth-token/", views.LoginView.as_view()),
    path("refresh-auth-token/", views.RefreshView.as_view()),
] + router.urls
