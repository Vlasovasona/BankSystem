from django import forms
from .models import Clients
from .models import Credits


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('client_code',)

class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        exclude = ('credit_code',)