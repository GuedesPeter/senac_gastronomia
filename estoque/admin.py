from django.contrib import admin
from .models import Categoria, Alimento, Entrada, Saida  # Removidos os modelos que não existem mais

# Registre seus modelos aqui.

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'validade', 'valor')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')
