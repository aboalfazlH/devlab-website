from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

django_urls = [
    path("admin/", admin.site.urls),
]
third_party_urls = [
    path("summernote/", include("django_summernote.urls")),
    path("select2/", include("django_select2.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
]
local_urls = [
    path("accounts/", include("apps.accounts.urls")),
    path("blog/", include("apps.blog.urls")),
    path("api/", include("apps.api.urls")),
    path("question-answer/", include("apps.qa.urls")),
    path("", include("apps.core.urls")),
]
urlpatterns = django_urls + third_party_urls + local_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
