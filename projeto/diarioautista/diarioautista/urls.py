from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from accounts import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),  # Rota para a página inicial
    path('index', views.inicio_view, name='inicio'),  # Rota para a página inicial
    path('ajuda', views.ajuda_view, name='ajuda'),  # Rota para a página de ajuda
    path('sobre', views.sobre_view, name='sobre'),  # Rota para a página Sobre
    path('service-worker.js', include('accounts.urls'), name='service-worker'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
