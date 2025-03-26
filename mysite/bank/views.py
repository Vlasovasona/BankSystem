# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, LoanTypes, Payroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, TemplateView
from django.db.models import Q


# Методы для работы с таблицей Clients

class ClientListView(ListView):
    queryset = Clients.objects.all()
    context_object_name = 'clients'
    paginate_by = 25
    template_name = 'bank/clients/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def client_detail(request, ID):
    """Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :param ID: Код клиента.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, client_code=ID)
    context = {
        'client': client,
    }
    return render(request, 'bank/clients/detail.html', context)

# class CreditsListView(ListView):
#     queryset = Credits.objects.all()
#     context_object_name = 'credits'
#     paginate_by = 3
#     template_name = 'bank/credits/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def credit_detail(request, credit_code):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param credit_code: Код кредита.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
#     credit = get_object_or_404(Credits, credit_code=credit_code)
#     context = {
#         'credit': credit,
#     }
#     return render(request, 'bank/credits/detail.html', context)
#
# class CreditTypesListView(ListView):
#     queryset = CreditType.objects.all()
#     context_object_name = 'credit_types'
#     paginate_by = 3
#     template_name = 'bank/creditTypes/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def credit_type_detail(request, credit_type_code):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param credit_type_code: Код типа кредита.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа кредита. """
#     credit_type = get_object_or_404(CreditType, credit_type_code=credit_type_code)
#     context = {
#         'credit_type': credit_type,
#     }
#     return render(request, 'bank/creditTypes/detail.html', context)
#
# class DepositsListView(ListView):
#     queryset = Deposits.objects.all()
#     context_object_name = 'deposits'
#     paginate_by = 3
#     template_name = 'bank/deposits/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def deposit_detail(request, deposit_code):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param deposit_code: Код кредита.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
#     deposit = get_object_or_404(Deposits, deposit_code=deposit_code)
#     context = {
#         'deposit': deposit,
#     }
#     return render(request, 'bank/deposits/detail.html', context)
#
# class DepositTypesListView(ListView):
#     queryset = DepositTypes.objects.all()
#     context_object_name = 'deposit_types'
#     paginate_by = 3
#     template_name = 'bank/depositTypes/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def deposit_type_detail(request, deposit_type_code):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param deposit_type_code: Код типа вклада.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
#     deposit_type = get_object_or_404(DepositTypes, deposit_type_code=deposit_type_code)
#     context = {
#         'deposit_type': deposit_type,
#     }
#     return render(request, 'bank/depositTypes/detail.html', context)
#
# class StatementOfDepositsListView(ListView):
#     queryset = StatementOfDeposits.objects.all()
#     context_object_name = 'statement_of_deposits'
#     paginate_by = 3
#     template_name = 'bank/statementOfDeposits/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def statement_of_deposits_detail(request, deposit_closing_number):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param deposit_closing_number: Код типа вклада.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
#     statement_item = get_object_or_404(StatementOfDeposits, deposit_closing_number=deposit_closing_number)
#     context = {
#         'statement_item': statement_item,
#     }
#     return render(request, 'bank/statementOfDeposits/detail.html', context)
#
# class CreditStatementListView(ListView):
#     queryset = CreditStatement.objects.all()
#     context_object_name = 'credit_statement'
#     paginate_by = 3
#     template_name = 'bank/creditStatement/list.html'
#
# # Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
# def credit_statement_detail(request, loan_repayment_number):
#     """Представление подробной информации о конкретном кредите.
#     :param request: HTTP-запрос.
#     :param loan_repayment_number: Код типа вклада.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
#     credit_statement_item = get_object_or_404(CreditStatement, loan_repayment_number=loan_repayment_number)
#     context = {
#         'credit_statement_item': credit_statement_item,
#     }
#     return render(request, 'bank/creditStatement/detail.html', context)
#
def search_clients(request):
    if request.method == 'POST':
        query = request.POST.get('search_query')
        clients = Clients.objects.filter(Q(name__icontains=query) | Q(familia__icontains=query) | Q(otchestvo__icontains=query))
        context = {'clients': clients}
        return render(request, 'bank/SQL-questions/clientsSearch.html', context)
    else:
        return render(request, 'bank/clients/list.html')