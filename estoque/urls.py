"""
------------------------------ ESTOQUE ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from .views import (
    AlimentoListView,
    AlimentoCreateView,
    AlimentoUpdateView,
    AlimentoDeleteView,
    UtilizarAlimentoView,
    EntradasListView,  
    SaidasListView,    
    EntradasPDFView,   
    SaidasPDFView,
    categoria_create,  # Importando a nova view para criar categorias
    
)

urlpatterns = [
    path('', AlimentoListView.as_view(), name='alimento_list'),  # Página principal listando os alimentos no estoque
    path('criar/', AlimentoCreateView.as_view(), name='alimento_create'),  # Adicionar novo alimento
    path('editar/<int:pk>/', AlimentoUpdateView.as_view(), name='alimento_update'),  # Editar alimento
    path('deletar/<int:pk>/', AlimentoDeleteView.as_view(), name='alimento_delete'),  # Deletar alimento
    path('utilizar/<int:pk>/', UtilizarAlimentoView.as_view(), name='utilizar_alimento'),  # Utilizar alimento (saída)
    path('entradas/', EntradasListView.as_view(), name='entradas_list'),  # Listar entradas
    path('saidas/', SaidasListView.as_view(), name='saidas_list'),  # Listar saídas
    path('entradas/pdf/', EntradasPDFView.as_view(), name='entradas_pdf'),  # Gerar PDF de entradas
    path('saidas/pdf/', SaidasPDFView.as_view(), name='saidas_pdf'),  # Gerar PDF de saídas
    path('categoria/criar/', categoria_create, name='categoria_create'),  # Adicionar nova categoria
    
]
