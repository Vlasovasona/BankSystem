from django import forms
from .models import Clients

familia = forms.CharField(max_length=25)
name = forms.CharField(max_length=25)
otchestvo = forms.CharField(max_length=25)



class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ('familia', 'name', 'age')