from django import forms
from .models import Clients
from .models import Credits, CreditType, Deposits, DepositTypes


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('client_code',)

class CreditsForm(forms.ModelForm):
    class Meta:
        model = Credits
        exclude = ('credit_code',)

class CreditTypesForm(forms.ModelForm):
    class Meta:
        model = CreditType
        exclude = ('credit_type_code',)

class DepositsForm(forms.ModelForm):
    class Meta:
        model = Deposits
        exclude = ('deposit_code',)

class DepositTypesForm(forms.ModelForm):
    class Meta:
        model = DepositTypes
        exclude = ('deposit_type_code',)