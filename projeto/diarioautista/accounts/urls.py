from django.urls import path
from . import views

urlpatterns = [
    path('service-worker.js', views.service_worker, name='service-worker'),
    path('login/', views.login_view, name='login'),  # Rota para a página de login
    path('perfil/', views.perfil, name='perfil'),  # Rota para a página de perfil
    path('editar/', views.perfil_editar, name='perfil_editar'),  # Rota para a página de edição do perfil
    path('cadastro/', views.cadastro_view, name='cadastro'), # Rota para a página de cadastro
    path('perfil/diario/', views.diario, name='perfil_diario'),
    path('perfil/diario/<int:postagem_id>/', views.visualizar_postagem, name='visualizar_postagem'),
    path('perfil/diario/nova/', views.nova_postagem, name='nova_postagem'),
    path('perfil/excluir', views.excluir_conta, name='excluir_conta'),
    path('perfil/diario/postagem/<int:postagem_id>/excluir/', views.excluir_postagem, name='excluir_postagem'),
    path('perfil/diario/relatorio', views.relatorio_analise, name='relatorio'),
]