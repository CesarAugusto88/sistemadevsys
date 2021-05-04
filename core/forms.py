from django import forms

from .models import (
    Arq, Bol, Chamado, Cliente, Funcionario,
    Ven_Caixa, Ven_Formas, Fin_Banco, Fin_Conta, Fin_SubConta,
    Ven_Fecha_Caixa, Con_Empresa)


class ArqForm(forms.ModelForm):
    class Meta:
        model = Arq
        fields = ('titulo', 'assunto', 'arquivo')


class BolForm(forms.ModelForm):
    class Meta:
        model = Bol
        fields = ('titulo', 'assunto', 'boleto', 'cliente')


class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ('nome_cliente', 'assunto', 'descricao', 'arquivo', 'funcionario')


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'referencial', 'nome', 'razao_social', 'tipo_pessoa', 'cpf_cnpj',
            'rg_ie', 'endereco', 'cep', 'uf', 'email', 'fone1', 'bloqueado',
            'chave', 'usuario_cli'
            )


# Para atualizar pelo funcionario
class ClienteFunForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'referencial', 'nome', 'razao_social', 'tipo_pessoa', 'cpf_cnpj', 'rg_ie',
            'endereco', 'cep', 'uf', 'email', 'fone1', 'bloqueado'
            )


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = (
            'referencial', 'nome', 'endereco', 'email', 'fone1', 'usuario_fun'
            )


############### Venda Caixa ##############
class Ven_CaixaForm(forms.ModelForm):
    class Meta:
        model = Ven_Caixa
        fields = (
            'referencial', 'data', 'troco', 'ref_fun',
            'fechado', 'hora_fechamento', 'nome_caixa', 'saldo'
            )

class Ven_FormasForm(forms.ModelForm):
    class Meta:
        model = Ven_Formas
        fields = (
            'referencial', 'nome', 'tipo'
            )

class Fin_BancoForm(forms.ModelForm):
    class Meta:
        model = Fin_Banco
        fields = (
            'referencial', 'banco', 'n_banco', 'n_agencia', 'n_conta',
            'digito_conta'
            )

class Fin_ContaForm(forms.ModelForm):
    class Meta:
        model = Fin_Conta
        fields = (
            'referencial', 'conta'
            )

class Fin_SubContaForm(forms.ModelForm):
    class Meta:
        model = Fin_SubConta
        fields = (
            'referencial', 'ref_conta', 'subconta', 'credito', 'debito',
            'pagar'
            )

class Ven_Fecha_CaixaForm(forms.ModelForm):
    class Meta:
        model = Ven_Fecha_Caixa
        fields = (
            'referencial', 'ref_caixa', 'ref_forma', 'ref_servicos',
            'valor', 'debito', 'complemento', 'ref_banco', 'desconto'
            )

class Con_EmpresaForm(forms.ModelForm):
    class Meta:
        model = Con_Empresa
        fields = (
            'referencial', 'nome', 'razao_social', 'cnpj'
            )