from django.conf.urls.static import static
from django.urls import path,include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('apps.accounts.urls')),
    path('blog/',include('apps.blog.urls')),
    path('',include('apps.core.urls')),
    path('api/',include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)