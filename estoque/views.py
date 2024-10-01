from decimal import Decimal
from django.contrib import messages
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


class AlimentoListView(ListView):
    model = Alimento
    template_name = 'estoque/estoque.html'
    context_object_name = 'alimentos'

    def get_queryset(self):
        queryset = Alimento.objects.all()  # Começa com todos os alimentos

        # Filtros
        categoria_id = self.request.GET.get('categoria')
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
        context['alimentos_vencidos'] = Alimento.objects.filter(validade__lt=now)
        context['categorias'] = Categoria.objects.all()  # Passa todas as categorias
        context['now'] = now  # Passa a data atual

        # Calculando o valor total por categoria
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            context['valor_total_categoria'] = Alimento.objects.filter(categoria_id=categoria_id).aggregate(Sum('valor'))['valor__sum'] or 0
            context['categoria_atual'] = Categoria.objects.get(id=categoria_id).nome  # Adiciona o nome da categoria atual
        else:
            context['valor_total_categoria'] = 0
            context['categoria_atual'] = "Nenhuma Categoria Selecionada"  # Indica que nenhuma categoria foi escolhida

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
            # Incrementa a quantidade, peso e valor do alimento existente
            alimento_existente.quantidade += quantidade
            alimento_existente.peso += peso
            alimento_existente.valor += (valor * quantidade)  # Multiplica o valor pela quantidade
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
            alimento.valor = valor * quantidade  # Atribui o valor multiplicado pela quantidade ao novo alimento
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
