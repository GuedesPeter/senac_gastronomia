"""
------------------------------ FINANCEIRO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from .views import financeiro, gerar_pdf

urlpatterns = [
    path('', financeiro, name='financeiro'),
    path('gerar_pdf/', gerar_pdf, name='gerar_pdf'),  # Adicione esta linha
=======
from .views import financeiro
from .views import dashboard


urlpatterns = [
    path('', financeiro, name='financeiro'),
    path('dashboard/', dashboard, name='dashboard')
    
>>>>>>> 511debd2956f28d34db39f8470da5fce68b4b2a7
]
