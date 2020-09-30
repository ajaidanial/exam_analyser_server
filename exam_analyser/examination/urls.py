from rest_framework.routers import SimpleRouter

from . import views

app_name = "examination"

router = SimpleRouter()
router.register("subjects", views.SubjectViewSet, basename="subject_viewset")
router.register("exams", views.ExamViewSet, basename="exam_viewset")
router.register(
    "question-categories",
    views.QuestionCategoryViewSet,
    basename="question_category_viewset",
)

urlpatterns = [] + router.urls
