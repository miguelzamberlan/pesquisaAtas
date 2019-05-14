from django.contrib import admin
from .models import Ata

# Register your models here.
@admin.register(Ata)
class AtaAdmin(admin.ModelAdmin):
    list_display = ['descricao_complementar_p1', 'descricao_complementar_p2', 'cod_cat', 'desc_catalogo', 'nome_cat', 'grupo_material', 'valor_unitario', 'gerenciador_nome', 'uf', 'certame', 'data_final_vigencia']
    #search_fields = ['descricao_complementar_p1', 'descricao_complementar_p2', 'nome_cat', 'desc_catalogo']
    search_fields = ['descricao_complementar_p1', 'descricao_complementar_p2', 'valor_unitario']
    #list_filter =  ['valor_unitario', 'gerenciador_nome', 'uf', 'data_final_vigencia']

