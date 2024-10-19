from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from xhtml2pdf import pisa  # Certifique-se de que a biblioteca xhtml2pdf está instalada

from .models import Alimento, Entrada, Saida, Categoria  # Certifique-se que os modelos estão definidos corretamente
from .forms import AlimentoForm, CategoriaForm  # Certifique-se que os forms estão definidos


def deslogar_view(request):
    logout(request)  # Desloga o usuário
    return redirect('sigin')  # Redireciona para a página de login (ou qualquer outra página)

def financeiro_view(request):
    # Adicione qualquer lógica que precisar aqui
    return render(request, 'financeiro.html')  # Isso vai renderizar o template financeiro.html

def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria Criada com Sucesso!')
            return redirect('alimento_list')  # Redireciona para a lista de alimentos após a criação
    else:
        form = CategoriaForm()

    return render(request, 'estoque/categoria_form.html', {'form': form})  # Renderiza um template específico para a criação


def itens_vencidos(request):
    # Obtém a data atual
    data_atual = timezone.now().date()
    
    # Obtém todas as categorias
    categorias = Categoria.objects.all()
    
    # Obtém a categoria selecionada, se houver
    categoria_selecionada = request.GET.get('categoria', None)
    
    # Filtra os itens vencidos
    if categoria_selecionada:
        itens_vencidos = Alimento.objects.filter(validade__lt=data_atual, categoria_id=categoria_selecionada)
    else:
        itens_vencidos = Alimento.objects.filter(validade__lt=data_atual)

    # Contagem de itens vencidos por categoria
    itens_por_categoria = {categoria.id: Alimento.objects.filter(validade__lt=data_atual, categoria=categoria).count() for categoria in categorias}

    # Total de itens vencidos na categoria selecionada ou todos os itens vencidos
    total_itens_vencidos_categoria = itens_por_categoria.get(int(categoria_selecionada), 0) if categoria_selecionada else itens_vencidos.count()

    # Obtem o nome da categoria selecionada, se houver
    categoria_nome = None
    if categoria_selecionada:
        categoria = get_object_or_404(Categoria, id=categoria_selecionada)
        categoria_nome = categoria.nome

    # Renderiza o template com os dados
    return render(request, 'estoque/itens_vencidos.html', {
        'itens_vencidos': itens_vencidos,
        'categorias': categorias,
        'itens_por_categoria': itens_por_categoria,
        'total_itens_vencidos_categoria': total_itens_vencidos_categoria,
        'categoria_nome': categoria_nome,  # Adiciona o nome da categoria ao contexto
    })



class AlimentoListView(ListView):
    model = Alimento
    template_name = 'estoque/estoque.html'
    context_object_name = 'alimentos'

    def get_queryset(self):
        queryset = Alimento.objects.filter(validade__gte=timezone.now().date())  # Filtra para incluir apenas alimentos não vencidos

        # Filtros
        categoria_id = self.request.GET.get('categoria') or self.request.session.get('categoria_selecionada')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        nome = self.request.GET.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        referencia = self.request.GET.get('referencia')
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)

        data_entrada = self.request.GET.get('data_entrada')
        if data_entrada:
            queryset = queryset.filter(data_entrada=data_entrada)

        nro_nota = self.request.GET.get('nro_nota')
        if nro_nota:
            queryset = queryset.filter(nro_nota__icontains=nro_nota)

        marca = self.request.GET.get('marca')
        if marca:
            queryset = queryset.filter(marca__icontains=marca)

        nome_fornecedor = self.request.GET.get('nome_fornecedor')
        if nome_fornecedor:
            queryset = queryset.filter(nome_fornecedor__icontains=nome_fornecedor)

        return queryset.order_by('nome')  # Ordena por nome

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now().date()
        alimentos_vencidos = Alimento.objects.filter(validade__lt=now)

        context['categorias'] = Categoria.objects.all()  # Passa todas as categorias
        context['now'] = now  # Passa a data atual

        # Verificando se há alimentos vencidos para a notificação e se a mensagem já foi exibida
        total_vencidos = alimentos_vencidos.count()
        mensagem_vista = self.request.session.get('mensagem_vista', False)

        if total_vencidos > 0 and not mensagem_vista:
            context['mensagem_vencidos'] = f"Atenção: Você possui {total_vencidos} alimento(s) vencido(s). Por favor, visualize a área de ITENS VENCIDOS."
            self.request.session['mensagem_vista'] = True  # Marca que a mensagem já foi visualizada
        else:
            context['mensagem_vencidos'] = None  # Limpa a mensagem se não houver alimentos vencidos ou se a mensagem já foi visualizada

        # Calculando o valor total por categoria
        categoria_id = self.request.GET.get('categoria') or self.request.session.get('categoria_selecionada')

        if categoria_id:
            context['valor_total_categoria'] = Alimento.objects.filter(categoria_id=categoria_id).aggregate(Sum('valor'))['valor__sum'] or 0
            context['categoria_atual'] = Categoria.objects.get(id=categoria_id).nome  # Adiciona o nome da categoria atual
            context['categoria_selecionada'] = categoria_id  # Passa a categoria selecionada para o template

            # Armazenar a categoria na sessão
            self.request.session['categoria_selecionada'] = categoria_id
        else:
            context['valor_total_categoria'] = 0
            context['categoria_atual'] = "Nenhuma Categoria Selecionada"  # Indica que nenhuma categoria foi escolhida
            context['categoria_selecionada'] = None  # Nenhuma categoria foi selecionada

        return context


class AlimentoCreateView(CreateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'estoque/alimento_create.html'
    success_url = reverse_lazy('alimento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Supondo que você tenha um modelo Categoria
        return context

    def form_valid(self, form):
        # Captura os dados dos campos
        categoria = form.cleaned_data.get('categoria')
        nome = form.cleaned_data.get('nome')
        referencia = form.cleaned_data.get('referencia')
        quantidade = form.cleaned_data.get('quantidade')
        peso = form.cleaned_data.get('peso')
        validade = form.cleaned_data.get('validade')
        nro_nota = form.cleaned_data.get('nro_nota')
        nome_fornecedor = form.cleaned_data.get('nome_fornecedor')
        marca = form.cleaned_data.get('marca')
        valor = form.cleaned_data.get('valor')  # Captura o valor do alimento

        # Verifica se o alimento com essa referência já existe no estoque
        alimento_existente = Alimento.objects.filter(nome=nome, referencia=referencia).first()

        if alimento_existente:
            # Incrementa a quantidade, peso e mantém o valor sem multiplicação
            alimento_existente.quantidade += quantidade
            alimento_existente.peso += peso
            alimento_existente.valor += valor  # Atribui o valor diretamente
            alimento_existente.save()

            # Registra a entrada do alimento existente
            entrada = Entrada(
                alimento=alimento_existente,
                quantidade=quantidade,
                peso=peso,
                validade=validade
            )
            entrada.save()

            # Atualiza o form para apontar para o alimento existente
            form.instance = alimento_existente
        else:
            # Salva o novo alimento com todos os campos
            alimento = form.save(commit=False)
            alimento.categoria = categoria  # Atribui a categoria ao novo alimento
            alimento.valor = valor  # Atribui o valor diretamente ao novo alimento
            alimento.save()

            # Registra a entrada do novo alimento
            entrada = Entrada(
                alimento=alimento,
                quantidade=quantidade,
                peso=peso,
                validade=validade
            )
            entrada.save()

        return super().form_valid(form)



class AlimentoUpdateView(UpdateView):
    model = Alimento
    form_class = AlimentoForm
    template_name = 'estoque/alimento_update.html'
    success_url = reverse_lazy('alimento_list')

    def form_valid(self, form):
        # Atualiza todos os campos do alimento
        alimento = form.save(commit=False)

        quantidade_atualizada = form.cleaned_data.get('quantidade')
        peso_atualizado = form.cleaned_data.get('peso')

        # Se a quantidade ou peso forem alterados, registrar a entrada
        if quantidade_atualizada > 0 or peso_atualizado > 0:
            entrada = Entrada(
                alimento=alimento,
                quantidade=quantidade_atualizada,
                peso=peso_atualizado,
                validade=alimento.validade  # Pode ajustar conforme necessário
            )
            entrada.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Supondo que você tenha um modelo Categoria
        return context


class UtilizarAlimentoView(View):
    def post(self, request, pk):
        alimento = get_object_or_404(Alimento, pk=pk)
        quantidade_utilizada = int(request.POST.get('quantidade', 0))
        peso_utilizado = Decimal(request.POST.get('peso', 0.0))

        if (quantidade_utilizada > 0 and quantidade_utilizada <= alimento.quantidade and
                peso_utilizado > 0 and peso_utilizado <= alimento.peso):
            # Calcula a proporção do valor a ser reduzido
            valor_por_unidade = alimento.valor / alimento.quantidade
            valor_utilizado = valor_por_unidade * quantidade_utilizada
            
            # Reduz a quantidade, peso e valor disponível do alimento
            alimento.quantidade -= quantidade_utilizada
            alimento.peso -= peso_utilizado
            alimento.valor -= valor_utilizado
            alimento.save()

            # Registra a saída do alimento utilizado
            saida = Saida(
                alimento=alimento,
                quantidade=quantidade_utilizada,
                peso=peso_utilizado,
                validade=alimento.validade  # Ajuste conforme necessário
            )
            saida.save()

        return redirect('alimento_list')


class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'estoque/alimento_delete.html'
    success_url = reverse_lazy('alimento_list')


class EntradasListView(ListView):
    model = Entrada
    template_name = 'estoque/entradas_list.html'  # Crie este template
    context_object_name = 'entradas'

    def get_queryset(self):
        return Entrada.objects.all().order_by('-validade')


class SaidasListView(ListView):
    model = Saida
    template_name = 'estoque/saidas_list.html'  # Crie este template
    context_object_name = 'saidas'

    def get_queryset(self):
        return Saida.objects.all().order_by('-validade')


class EntradasPDFView(View):
    def get(self, request, *args, **kwargs):
        entradas = Entrada.objects.all()
        template = 'estoque/entradas_pdf.html'  # Crie este template

        context = {
            'entradas': entradas,
        }

        html = render_to_string(template, context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="entradas.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Erro ao gerar PDF.')

        return response


class SaidasPDFView(View):
    def get(self, request, *args, **kwargs):
        saidas = Saida.objects.all()
        template = 'estoque/saidas_pdf.html'  # Crie este template

        context = {
            'saidas': saidas,
        }

        html = render_to_string(template, context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="saidas.pdf"'
        
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Erro ao gerar PDF.')

        return response


