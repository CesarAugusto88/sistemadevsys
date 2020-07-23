from django import forms

from .models import Arq


class ArqForm(forms.ModelForm):
    class Meta:
        model = Arq
        fields = ('titulo', 'assunto', 'arquivo', 'imagem')