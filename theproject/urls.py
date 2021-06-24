from django.urls import include, path
from django.contrib import admin
# from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404, handler500, handler403


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theapp.urls')),
]

# ERROR PAGES

handler500 = 'theapp.views.custom_error_500'

handler404 = 'theapp.views.custom_error_404'

handler403 = 'theapp.views.custom_error_403'


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
