from django.shortcuts import render

# Create your views here.


def estoque(request):
    return render(request, 'estoque/estoque.html')  