from django import forms
from .models import Clients
from .models import Credits, CreditType, Deposits, DepositTypes, StatementOfDeposits, CreditStatement


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

class StatementOfDepositsForm(forms.ModelForm):
    class Meta:
        model = StatementOfDeposits
        exclude = ('deposit_closing_number',)

class CreditStatementForm(forms.ModelForm):
    class Meta:
        model = CreditStatement
        exclude = ('loan_repayment_number',)