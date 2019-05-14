from django import forms
from .models import Ata

class PostForm(forms.ModelForm):

    class Meta:
        model = Ata
        #fields = ('descricao_complementar_p1', 'descricao_complementar_p2', 'valor_unitario')
