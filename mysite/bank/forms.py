from django import forms
from .models import CreditStatement, LoanTypes, Clients, Payroll, AuthUser
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


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


# Форма для регистрации нового пользователя
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

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['first_name', 'last_name', 'email']  # Включайте нужные поля

    def clean_email(self):
        """Валидация электронного адреса."""
        email = self.cleaned_data.get('email')
        if not email or '@' not in email:
            raise forms.ValidationError("Неверный формат электронной почты.")
        return email

    def clean_first_name(self):
        """Валидация имени."""
        first_name = self.cleaned_data.get('first_name')
        # Проверка на соответствие только русским буквам
        if not re.match(r'^([А-Яа-я]+)$', first_name):
            raise forms.ValidationError("Имя должно содержать только русские буквы.")
        return first_name

    def clean_last_name(self):
        """Валидация фамилии."""
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^([А-Яа-я]+)$', last_name):
            raise forms.ValidationError("Фамилия должна содержать только русские буквы.")
        return last_name