from django import forms
from .models import CreditStatement, LoanTypes, Clients, Payroll
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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



# Формы для регистрации нового пользователя
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='Email', required=True)
    is_staff = forms.BooleanField(label='Администратор?', required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user