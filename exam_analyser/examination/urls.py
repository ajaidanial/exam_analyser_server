from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "examination"

router = SimpleRouter()
router.register("subjects", views.SubjectViewSet, basename="subject_viewset")
router.register("questions", views.QuestionViewSet, basename="question_viewset")
router.register(
    "question-papers", views.QuestionPaperViewSet, basename="question_paper_viewset"
)
router.register("exams", views.ExamViewSet, basename="exam_viewset")
router.register(
    "question-categories",
    views.QuestionCategoryViewSet,
    basename="question_category_viewset",
)

urlpatterns = [
    path(
        "exam-subject-overview/",
        views.ExamSubjectOverviewView.as_view(),
        name="exam_subject_overview_view",
    ),
    path(
        "dashboard-insights/",
        views.DashboardDataAPIView.as_view(),
        name="dashboard_insights_view",
    ),
    path(
        "marks-upload/",
        views.QuestionPaperMarksUploadView.as_view(),
        name="marks_upload_view",
    ),
    path(
        "<str:pk>/report-card/",
        views.UserReportCardView.as_view(),
        name="report_cards_view",
    ),
] + router.urls
