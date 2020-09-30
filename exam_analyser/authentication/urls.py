from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("get-auth-token/", views.LoginView.as_view()),
    path("refresh-auth-token/", views.RefreshView.as_view()),
]
