"""
------------------------------ FINANCEIRO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from .views import financeiro, gerar_pdf

urlpatterns = [
    path('', financeiro, name='financeiro'),
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),  # Adicione esta linha
]
