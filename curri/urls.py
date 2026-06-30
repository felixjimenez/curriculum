from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    # Antes de admin/ para que /admin/visitas/ no lo capture el panel de Django.
    path('admin/visitas/', core_views.admin_visitas, name='admin_visitas'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Servir media localmente (dev o VPS con USE_LOCAL_MEDIA=True)
if settings.DEBUG or getattr(settings, 'USE_LOCAL_MEDIA', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)