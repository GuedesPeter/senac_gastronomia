from django import forms
from .models import Alimento, Categoria

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = [
            'categoria', 'referencia', 'nome', 'quantidade',
            'peso', 'validade', 'valor', 'data_entrada',
            'nro_nota', 'nome_fornecedor', 'marca'
        ]
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'validade': forms.DateInput(attrs={'type': 'date'}),
        }



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
