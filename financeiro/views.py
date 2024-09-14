from django.shortcuts import render

# Create your views here.


def financeiro(request):
    return render(request, 'financeiro/financeiro.html')  
