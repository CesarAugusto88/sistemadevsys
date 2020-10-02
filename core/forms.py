from django import forms

from .models import Arq, Bol, Chamado, Cliente, Funcionario


class ArqForm(forms.ModelForm):
    class Meta:
        model = Arq
        fields = ('titulo', 'assunto', 'arquivo', 'imagem')

class BolForm(forms.ModelForm):
    class Meta:
        model = Bol
        fields = ('titulo', 'assunto', 'boleto', 'imagem', 'cliente')

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ('nome_cliente', 'assunto', 'descricao', 'arquivo', 'funcionario')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nome', 'razao_social', 'tipo_pessoa', 'cpf_cnpj', 'rg_ie',
            'endereco', 'cep', 'uf', 'email', 'fone1', 'bloqueado', 'usuario_cli'
            )

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = (
            'nome', 'endereco', 'email', 'fone1', 'usuario_fun'
            )