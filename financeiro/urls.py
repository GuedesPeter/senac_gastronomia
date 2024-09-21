"""
------------------------------ FINANCEIRO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from .views import financeiro


urlpatterns = [
    path('', financeiro, name='financeiro'),
    
]
