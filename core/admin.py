from django.contrib import admin
from core.models import Funcionario, Cliente, Ordem_Servico, Arq

class Arq_Admin(admin.ModelAdmin):    
    list_display = ('titulo','assunto')
    search_fields = ['titulo']


class Func_Admin(admin.ModelAdmin):
    list_display = ('id','nome', 'cpf', 'cargo', 'fone1')
    list_filter = ('bairro', 'email',)
    ordering = ['nome']
    search_fields = ['nome', 'id']
    
    

class Cli_Admin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'razao_social', 'cpf_cnpj', 'celular')
    list_filter = ('celular', 'email',)
    ordering = ['nome']
    search_fields = ['nome', 'id']

class OS_Admin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'descricao', 'dt_entrada', 'responsavel')
    list_filter = ('dt_entrada',)
    ordering = ['dt_entrada']
    search_fields = ['dt_agenda', 'descricao', 'id']

""" tabela no models (colocar Visitante no import)
class Vis_Admin(admin.ModelAdmin):
    list_display = ('id', 'nome',  'cpf', 'fone1')
    list_filter = ('bairro', 'email',)
    ordering = ['nome']
    search_fields = ['nome', 'id']
admin.site.register(Visitante, Vis_Admin)
"""

admin.site.register(Funcionario, Func_Admin)
admin.site.register(Cliente, Cli_Admin)
admin.site.register(Ordem_Servico, OS_Admin)
admin.site.register(Arq, Arq_Admin)
