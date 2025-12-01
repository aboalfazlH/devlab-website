from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path("summernote/", include("django_summernote.urls")),
    path("select2/", include("django_select2.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("blog/", include("apps.blog.urls")),
    path("api/", include("apps.api.urls")),
    path("question-answer/", include("apps.qa.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
