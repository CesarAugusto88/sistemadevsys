from django.contrib import admin
from django.contrib.auth.models import Group
from core.models import (Arq, Bol, Cliente, Funcionario, Ordem_Servico,
                        Chamado, Ven_Caixa, Ven_Formas, Fin_Banco, Fin_Conta,
                        Fin_SubConta, Ven_Fecha_Caixa, Con_Empresa)


admin.site.site_header = 'Admin DevSys Dashboard'


class Chamado_Admin(admin.ModelAdmin):    
    list_display = ('nome_cliente','assunto', 'dt_entrada')
    search_fields = ['nome_cliente']


class Arq_Admin(admin.ModelAdmin):    
    list_display = ('titulo','assunto')
    search_fields = ['titulo']

class Bol_Admin(admin.ModelAdmin):    
    list_display = ('titulo','assunto')
    search_fields = ['titulo']


class Func_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'nome', 'cpf', 'cargo', 'fone1')
    list_filter = ('referencial', 'bairro', 'email',)
    ordering = ['nome']
    search_fields = ['nome', 'id', 'referencial']


class Cli_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'nome', 'razao_social', 'cpf_cnpj',
                    'celular')
    list_filter = ('referencial', 'celular', 'email',)
    ordering = ['nome']
    search_fields = ['nome', 'id', 'referencial']


class OS_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'valor', 'descricao', 'dt_atualizada',
                    'responsavel')
    list_filter = ('dt_atualizada', 'referencial',)
    ordering = ['dt_atualizada']
    search_fields = ['dt_agenda', 'descricao', 'id', 'referencial']


# Venda Caixa
class Ven_Caixa_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'data', 'troco', 'ref_fun',
                    'fechado', 'hora_fechamento', 'nome_caixa',
                    'saldo_final')
    list_filter = ('referencial', 'data')
    ordering = ['id']
    search_fields = ['data',  'referencial',]


class Ven_Formas_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'nome', 'tipo',)
    list_filter = ('referencial', 'nome')
    ordering = ['id']
    search_fields = ['referencial', 'nome', 'tipo',]


class Fin_Banco_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'banco', 'n_banco', 'n_agencia',
                    'n_conta', 'digito_conta',)
    list_filter = ('referencial', 'banco')
    ordering = ['id']
    search_fields = ['referencial', 'banco',]


class Fin_Conta_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'conta',)
    list_filter = ('referencial', 'conta')
    ordering = ['id']
    search_fields = ['referencial', 'conta',]


class Fin_SubConta_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'ref_conta', 'subconta',
                    'credito', 'debito', 'pagar')
    list_filter = ('referencial', 'subconta')
    ordering = ['id']
    search_fields = ['referencial', 'subconta',]


class Ven_Fecha_Caixa_Admin(admin.ModelAdmin):
    list_display = ( 'id', 'referencial', 'ref_caixa',
                    'ref_forma',  'valor', 'debito', 'complemento',
                    'ref_banco', 'desconto')
    list_filter = ( 'referencial', 'complemento')
    ordering = ['id']
    search_fields = ['data', 'complemento', 'referencial',]


class Con_Empresa_Admin(admin.ModelAdmin):
    list_display = ('id', 'referencial', 'nome', 'razao_social', 'cnpj',)
    list_filter = ( 'referencial', 'cnpj')
    ordering = ['id']
    search_fields = ['referencial', 'nome',]


admin.site.register(Chamado, Chamado_Admin)
admin.site.register(Funcionario, Func_Admin)
admin.site.register(Cliente, Cli_Admin)
admin.site.register(Ordem_Servico, OS_Admin)
admin.site.register(Arq, Arq_Admin)
admin.site.register(Bol, Bol_Admin)

admin.site.register(Ven_Caixa, Ven_Caixa_Admin)
admin.site.register(Ven_Formas, Ven_Formas_Admin)
admin.site.register(Fin_Banco, Fin_Banco_Admin)
admin.site.register(Fin_Conta, Fin_Conta_Admin)
admin.site.register(Fin_SubConta, Fin_SubConta_Admin)
admin.site.register(Ven_Fecha_Caixa, Ven_Fecha_Caixa_Admin)
admin.site.register(Con_Empresa, Con_Empresa_Admin)


admin.site.unregister(Group)
