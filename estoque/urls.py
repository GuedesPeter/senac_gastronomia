"""
------------------------------ ESTOQUE ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from autenticacao.views import estoque

urlpatterns = [
    path('', estoque, name='estoque'),
    
]

