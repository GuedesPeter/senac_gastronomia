from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Alimento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='alimentos')
    referencia = models.CharField(max_length=100)
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField()
    nro_nota = models.CharField(max_length=100)
    nome_fornecedor = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.referencia}"


class Entrada(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data = models.DateField(default=timezone.now)  # Usando a data atual como padrão

    def __str__(self):
        return f"Entrada: {self.alimento.nome}"


class Saida(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='saidas')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()
    data = models.DateField(default=timezone.now)  # Usando a data atual como padrão

    def __str__(self):
        return f"Saída: {self.alimento.nome}"