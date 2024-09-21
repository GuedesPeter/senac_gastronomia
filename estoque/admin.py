from django.contrib import admin
# from .models import Alimento
from .models import Categoria, Alimento
# Register your models here.

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantidade', 'validade', 'valor')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)