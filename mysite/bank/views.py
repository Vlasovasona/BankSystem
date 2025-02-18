# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, Credits, CreditType, Deposits
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, TemplateView


# Методы для работы с таблицей Clients

class ClientListView(ListView):
    queryset = Clients.objects.all()
    context_object_name = 'clients'
    paginate_by = 3
    template_name = 'bank/clients/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def client_detail(request, client_code):
    """Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :param client_code: Код клиента.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, client_code=client_code)
    context = {
        'client': client,
    }
    return render(request, 'bank/clients/detail.html', context)

class CreditsListView(ListView):
    queryset = Credits.objects.all()
    context_object_name = 'credits'
    paginate_by = 3
    template_name = 'bank/credits/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def credit_detail(request, credit_code):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param credit_code: Код кредита.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    credit = get_object_or_404(Credits, credit_code=credit_code)
    context = {
        'credit': credit,
    }
    return render(request, 'bank/credits/detail.html', context)

class CreditTypesListView(ListView):
    queryset = CreditType.objects.all()
    context_object_name = 'credit_types'
    paginate_by = 3
    template_name = 'bank/creditTypes/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def credit_type_detail(request, credit_type_code):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param credit_type_code: Код типа кредита.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа кредита. """
    credit_type = get_object_or_404(CreditType, credit_type_code=credit_type_code)
    context = {
        'credit_type': credit_type,
    }
    return render(request, 'bank/creditTypes/detail.html', context)

class DepositsListView(ListView):
    queryset = Deposits.objects.all()
    context_object_name = 'deposits'
    paginate_by = 3
    template_name = 'bank/deposits/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def deposit_detail(request, deposit_code):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param deposit_code: Код кредита.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    deposit = get_object_or_404(Deposits, deposit_code=deposit_code)
    context = {
        'deposit': deposit,
    }
    return render(request, 'bank/deposits/detail.html', context)