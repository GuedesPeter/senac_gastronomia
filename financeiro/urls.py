"""
------------------------------ FINANCEIRO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from .views import financeiro
from .views import dashboard


urlpatterns = [
    path('', financeiro, name='financeiro'),
    path('dashboard/', dashboard, name='dashboard')
    
]
