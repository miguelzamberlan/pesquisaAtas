from django.db import models

# Create your models here.

class Ata(models.Model):
    gerenciador = models.IntegerField()
    gerenciador_nome = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    modalidade = models.CharField(max_length=200)
    certame = models.CharField(max_length=200)
    cnpj_fornecedor = models.CharField(max_length=200)
    nome_fornecedor = models.CharField(max_length=200)
    porte_fornecedor = models.CharField(max_length=200)
    munic_fornecedor = models.CharField(max_length=200)
    uf_fornecedor = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    cod_cat = models.CharField(max_length=200)
    nome_cat = models.TextField()
    desc_catalogo = models.TextField()
    grupo_material = models.CharField(max_length=200)
    data_homologacao = models.CharField(max_length=200)
    data_final_vigencia = models.DateField()
    prorrogacao_ata = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    descricao_complementar_p1 = models.TextField()
    descricao_complementar_p2 = models.TextField()
    fabricante = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    unidade = models.CharField(max_length=200)
    qtd_ofertada = models.IntegerField()
    valor_unitario = models.FloatField()
    valor_total = models.FloatField()

    def __str__(self):
        return self.descricao_complementar_p1
