"""
------------------------------ FINANCEIRO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
=======
#from autenticacao.views import financeiro
>>>>>>> a3a7816afa6f92e3b255ac7a2084968ecd62a183
from .views import financeiro

urlpatterns = [
    path('', financeiro, name='financeiro'),
    
]
