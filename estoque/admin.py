from django.contrib import admin
from .models import Categoria, Alimento, AlimentoDevolucao, Entrada, Saida, EntradaDevolucao, SaidaDevolucao, Etiqueta, AlimentoVencido

# Register your models here.

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'validade', 'valor')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(AlimentoDevolucao)
class AlimentoDevolucaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'validade', 'valor')

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')

@admin.register(EntradaDevolucao)
class EntradaDevolucaoAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')

@admin.register(SaidaDevolucao)
class SaidaDevolucaoAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade')

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'alimento_devolucao', 'quantidade', 'peso', 'validade')

@admin.register(AlimentoVencido)
class AlimentoVencidoAdmin(admin.ModelAdmin):
    list_display = ('alimento', 'quantidade', 'peso', 'validade_venc', 'valor')
