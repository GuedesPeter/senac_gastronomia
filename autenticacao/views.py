from django.contrib import messages
# from django.contrib.auth import login, logout, Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

# Create your views here.


# class HomeView(TemplateView):
#     template_name = 'autenticacao/home.html'


class SigupView(TemplateView):
    template_name = 'autenticacao/sigup.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {'error_message': 'Usuário já existe.'})

        # Verifica se as senhas são iguais
        if password1 != password2:
            return render(request, self.template_name, {'error_message': 'As senhas não coincidem.'})

        # Se chegou até aqui, cria o usuário
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Redireciona para a página 'home.html' após o cadastro bem-sucedido, DEVERÁ REDIRECIONAR PARA A LISTA.
        return redirect('home')


class SiginView(TemplateView):
    template_name = 'autenticacao/sigin.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se os campos estão vazios
        if not username or not password:
            messages.error(request, 'Nome de usuário e senha são obrigatórios.')
            return redirect('sigin')

        # Autenticar o usuário
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login bem-sucedido, redireciona para a página inicial
            login(request, user)
            return redirect('escolha') 
        else:
            # Exibir mensagem de erro se o login falhar/ redireciona para login
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            return redirect('sigin')
        
class EscolhaView(TemplateView):
    template_name = 'autenticacao/escolha.html'

class ExitView(TemplateView):
    template_name = 'autenticacao/exit.html'

    def post(self, request, *args, **kwargs):
        # Realiza o logout do usuário
        logout(request)
        # Redireciona para a página inicial após o logout
        return redirect('sigin')