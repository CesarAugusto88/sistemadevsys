from django import forms

from .models import Arq, Bol


class ArqForm(forms.ModelForm):
    class Meta:
        model = Arq
        fields = ('titulo', 'assunto', 'arquivo', 'imagem')

class BolForm(forms.ModelForm):
    class Meta:
        model = Bol
        fields = ('titulo', 'assunto', 'boleto', 'imagem', 'cliente')
