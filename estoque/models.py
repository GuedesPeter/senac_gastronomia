from django.db import models


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


class AlimentoDevolucao(models.Model):
    categoria_dev = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='alimentos_devolvidos')
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
        return f"Devolução: {self.nome} - {self.referencia}"


class Entrada(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()

    def __str__(self):
        return f"Entrada: {self.alimento.nome}"


class Saida(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='saidas')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()

    def __str__(self):
        return f"Saída: {self.alimento.nome}"


class EntradaDevolucao(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='entradas_devolucao')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()

    def __str__(self):
        return f"Entrada Devolução: {self.alimento.nome}"


class SaidaDevolucao(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='saidas_devolucao')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField()

    def __str__(self):
        return f"Saída Devolução: {self.alimento.nome}"


class Etiqueta(models.Model):
    categoria_etiq = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='etiquetas')
    alimento_devolucao = models.ForeignKey(AlimentoDevolucao, on_delete=models.CASCADE, related_name='etiquetas')
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
        return f"Etiqueta: {self.nome} - {self.alimento_devolucao.referencia}"


class AlimentoVencido(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE, related_name='alimentos_vencidos')
    quantidade = models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    validade_venc = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateField()
    nro_nota = models.CharField(max_length=100)
    nome_fornecedor = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return f"Alimento Vencido: {self.alimento.nome} - {self.alimento.referencia}"
