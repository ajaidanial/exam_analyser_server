from rest_framework.routers import SimpleRouter

from . import views

app_name = "examination"

router = SimpleRouter()
router.register("subjects", views.SubjectViewSet, basename="subject_viewset")

urlpatterns = [] + router.urls
