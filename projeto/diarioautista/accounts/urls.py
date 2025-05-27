Importação dos módulos necessários
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Rota para a página de login
    path('perfil/', views.perfil, name='perfil'),  # Rota para a página de perfil
    path('editar/', views.perfil_editar, name='perfil_editar'),  # Rota para a página de edição do perfil
    path('cadastro/', views.cadastro_view, name='cadastro'), # Rota para a página de cadastro
    path('perfil/diario/', views.diario, name='perfil_diario'), # Rota para a página do diário
    path('perfil/diario/<int:postagem_id>/', views.visualizar_postagem, name='visualizar_postagem'), # Página de visualização de postagem
    path('perfil/diario/nova/', views.nova_postagem, name='nova_postagem'), # Formulário de nova postagem
    path('perfil/excluir', views.excluir_conta, name='excluir_conta'), # Função de exclusão da conta
    path('perfil/diario/postagem/<int:postagem_id>/excluir/', views.excluir_postagem, name='excluir_postagem'), # Função de exclusão da postagem
    path('perfil/diario/relatorio', views.relatorio_analise, name='relatorio'), # Exibição do relatório emocional
]
