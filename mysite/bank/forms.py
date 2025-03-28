from django import forms
from .models import CreditStatement, LoanTypes, Clients, Payroll
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        exclude = ('id',)

class CreditTypesForm(forms.ModelForm):
    class Meta:
        model = LoanTypes
        exclude = ('id',)


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        exclude = ('id',)

class CreditStatementForm(forms.ModelForm):
    class Meta:
        model = CreditStatement
        exclude = ('id',)
