"""
------------------------------ AUTENTICAÇÃO ---------------------------------

"""

from django.contrib import admin
from django.urls import path
from autenticacao.views import SigupView, SiginView, EscolhaView, ExitView

urlpatterns = [
    path('', SiginView.as_view(), name='sigin'),
    path('sigup/', SigupView.as_view(), name='sigup'),
    path('exit/', ExitView.as_view(), name='exit'),
    path('escolha/',EscolhaView.as_view(), name='escolha'),
]
