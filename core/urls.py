from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from orders.views import test_email
from . import views
from courses.views import accueil

urlpatterns = [
    path('', accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='accueil.html'), name='accueil'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('orders/', include('orders.urls')),
    path('dashboard/', include('dashboard.urls')),
     # ... vos URLs existantes ...
    path('test-email/', test_email, name='test_email'),
    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
