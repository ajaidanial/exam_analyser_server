from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Main URLS
# ------------------------------------------------------------------------------
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "ping",
        lambda r: HttpResponse("pong!"),
        name="ping",
    ),
    path(
        "auth/",
        include("exam_analyser.authentication.urls", namespace="authentication"),
    ),
    path(
        "examination/",
        include("exam_analyser.examination.urls", namespace="examination"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# static files serving when in local dev
# ------------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# documentation
# ------------------------------------------------------------------------------
schema_view = get_schema_view(
    openapi.Info(
        title="Exam Analyser - Documentation",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path("docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

# debug tool bar
# ------------------------------------------------------------------------------
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# silk debug tool
# ------------------------------------------------------------------------------
if settings.DEBUG and "silk" in settings.INSTALLED_APPS:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk_debug_tool"))]
