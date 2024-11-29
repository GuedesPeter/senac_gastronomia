from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import render
from estoque.models import Alimento
from datetime import datetime
from django.db.models import Sum
from .models import Alimento, Categoria
from django.core.paginator import Paginator

def financeiro(request):
    # Obter os parâmetros de filtragem e ordenação da URL
    categoria = request.GET.get('categoria', '')
    validade = request.GET.get('validade', '')
    data_entrada = request.GET.get('data_entrada', '')
    fornecedor = request.GET.get('fornecedor', '')
    marca = request.GET.get('marca', '')
    nome = request.GET.get('nome', '')
    ordenar_por = request.GET.get('ordenar_por', 'nome')  # Coluna padrão para ordenar

    def converter_data(data_brasileira):
        try:
            return datetime.strptime(data_brasileira, '%d/%m/%Y').date()
        except ValueError:
            return None

    # Aplicar filtros
    alimentos = Alimento.objects.all()

    if categoria:
        alimentos = alimentos.filter(categoria__nome__icontains=categoria)
    if validade:
        validade_convertida = converter_data(validade)
        if validade_convertida:
            alimentos = alimentos.filter(validade=validade_convertida)
    if data_entrada:
        data_entrada_convertida = converter_data(data_entrada)
        if data_entrada_convertida:
            alimentos = alimentos.filter(data_entrada=data_entrada_convertida)
    if fornecedor:
        alimentos = alimentos.filter(nome_fornecedor__icontains=fornecedor)
    if marca:
        alimentos = alimentos.filter(marca__icontains=marca)
    if nome:
        alimentos = alimentos.filter(nome__icontains=nome)

    # Ordenar alimentos
    alimentos = alimentos.order_by(ordenar_por)

    # Paginação: exibir 10 produtos por página
    paginator = Paginator(alimentos, 10)  # 10 produtos por página
    page_number = request.GET.get('page')  # Número da página atual
    page_obj = paginator.get_page(page_number)

    # Calcular métricas
    quantidade_total = sum([alimento.quantidade for alimento in alimentos])
    custo_total = sum([alimento.valor * alimento.quantidade for alimento in alimentos])
    
        # Obter todas as categorias
    categorias = Categoria.objects.all()

    # Contexto para o template
    context = {
        'page_obj': page_obj,  # Passar a página paginada
        'quantidade_total': quantidade_total,
        'custo_total': custo_total,
        'categoria': categoria,
        'validade': validade,
        'data_entrada': data_entrada,
        'fornecedor': fornecedor,
        'marca': marca,
        'nome': nome,
        'ordenar_por': ordenar_por,
        'categorias': categorias  # Adicionando categorias ao contexto
    }
    
    return render(request, 'financeiro/financeiro.html', context)


def gerar_pdf(request):
    # Obter os parâmetros de filtragem e ordenação da URL
    categoria = request.GET.get('categoria', '')
    validade = request.GET.get('validade', '')
    data_entrada = request.GET.get('data_entrada', '')
    fornecedor = request.GET.get('fornecedor', '')
    marca = request.GET.get('marca', '')
    nome = request.GET.get('nome', '')
    ordenar_por = request.GET.get('ordenar_por', 'nome')

    def converter_data(data_brasileira):
        try:
            return datetime.strptime(data_brasileira, '%d/%m/%Y').date()
        except ValueError:
            return None
        
    # Aplicar filtros
    alimentos = Alimento.objects.all()
    if categoria:
        alimentos = alimentos.filter(categoria__nome__icontains=categoria)
    if validade:
        validade_convertida = converter_data(validade)
        if validade_convertida:
            alimentos = alimentos.filter(validade=validade_convertida)
    if data_entrada:
        data_entrada_convertida = converter_data(data_entrada)
        if data_entrada_convertida:
            alimentos = alimentos.filter(data_entrada=data_entrada_convertida)
    if fornecedor:
        alimentos = alimentos.filter(nome_fornecedor__icontains=fornecedor)
    if marca:
        alimentos = alimentos.filter(marca__icontains=marca)
    if nome:
        alimentos = alimentos.filter(nome__icontains=nome)

    # Ordenar alimentos
    alimentos = alimentos.order_by(ordenar_por)

    # Calcular métricas
    quantidade_total = sum([alimento.quantidade for alimento in alimentos])
    custo_total = sum([alimento.valor * alimento.quantidade for alimento in alimentos])

    # Contexto para o template
    context = {
        'alimentos': alimentos,
        'quantidade_total': quantidade_total,
        'custo_total': custo_total,
        'categoria': categoria,
        'validade': validade,
        'data_entrada': data_entrada,
        'fornecedor': fornecedor,
        'marca': marca,
        'nome': nome,
        'ordenar_por': ordenar_por
    }

    # Carregar o template HTML para o PDF
    template_path = 'financeiro/produtos_pdf.html'  # Crie este template
    template = get_template(template_path)
    html = template.render(context)

    # Configurar a resposta do PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'

    # Criar o PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar erros
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response

# DASHBOARD VIEW
def dashboard(request):
    alimentos = Alimento.objects.all()
    # Calcular totais
    quantidade_total = sum([alimento.quantidade for alimento in alimentos])
    custo_total = sum([alimento.valor * alimento.quantidade for alimento in alimentos])

    # Calcular métricas por categoria e fornecedor
    categoria_data = alimentos.values('categoria__nome').annotate(total=Sum('quantidade'))
    fornecedor_data = alimentos.values('nome_fornecedor').annotate(total=Sum('quantidade'))

    # Preparar listas para o contexto
    categoria_labels = [data['categoria__nome'] for data in categoria_data]
    categoria_totals = [data['total'] for data in categoria_data]

    fornecedor_labels = [data['nome_fornecedor'] for data in fornecedor_data]
    fornecedor_totals = [data['total'] for data in fornecedor_data]

    # Contexto para o template
    context = {
        'categoria_labels': categoria_labels,
        'categoria_totals': categoria_totals,
        'fornecedor_labels': fornecedor_labels,
        'fornecedor_totals': fornecedor_totals,
        'quantidade_total': quantidade_total,
        'custo_total': custo_total,
    }

    return render(request, 'financeiro/dashboard.html', context)