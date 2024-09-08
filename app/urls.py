"""
------------------------------ GERAL ---------------------------------

"""

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')), # URLs de Autenticação
    path('estoque/', include('estoque.urls')), # URLs de Estoque
    path('financeiro/', include('financeiro.urls')), # URLs de Financeiro

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
