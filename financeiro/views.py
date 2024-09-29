from django.shortcuts import render

# Create your views here.


# def financeiro(request):
#     return render(request, 'financeiro/financeiro.html')  
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import render
from estoque.models import Alimento
from datetime import datetime

def financeiro(request):
    # Obter os parâmetros de filtragem e ordenação da URL
    categoria = request.GET.get('categoria', '')
    validade = request.GET.get('validade', '')
    data_entrada = request.GET.get('data_entrada', '')
    fornecedor = request.GET.get('fornecedor', '')
    marca = request.GET.get('marca', '')
    ordenar_por = request.GET.get('ordenar_por', 'nome')  # Coluna padrão para ordenar

    # Função para converter data no formato brasileiro (dd/mm/aaaa) para formato ISO (aaaa-mm-dd)
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

    # Ordenar alimentos
    alimentos = alimentos.order_by(ordenar_por)

    # Calcular métricas
    # Resultado de quantidade por linha
    # quantidade_total = alimentos.count()
   
    # Resultado de quantidade por total
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
        'ordenar_por': ordenar_por
    }

    return render(request, 'financeiro/financeiro.html', context)


def gerar_pdf(request):
    # Obter os parâmetros de filtragem e ordenação da URL
    categoria = request.GET.get('categoria', '')
    validade = request.GET.get('validade', '')
    data_entrada = request.GET.get('data_entrada', '')
    fornecedor = request.GET.get('fornecedor', '')
    marca = request.GET.get('marca', '')
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



