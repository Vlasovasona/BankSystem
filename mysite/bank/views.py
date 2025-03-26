# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, LoanTypes, Payroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect




# Методы для работы с таблицей Clients

class ClientListView(ListView):
    queryset = Clients.objects.all()
    context_object_name = 'clients'
    paginate_by = 25
    template_name = 'bank/clients/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def client_detail(request, id):
    """Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :param ID: Код клиента.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, id=id)
    context = {
        'client': client,
    }
    return render(request, 'bank/clients/detail.html', context)


class CreditTypesListView(ListView):
    queryset = LoanTypes.objects.all()
    context_object_name = 'credit_types'
    paginate_by = 25
    template_name = 'bank/creditTypes/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def credit_type_detail(request, id):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param id: Код типа кредита.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа кредита. """
    credit_type = get_object_or_404(LoanTypes, id=id)
    context = {
        'credit_type': credit_type,
    }
    return render(request, 'bank/creditTypes/detail.html', context)


class CreditStatementListView(ListView):
    queryset = CreditStatement.objects.all()
    context_object_name = 'credit_statement'
    paginate_by = 25
    template_name = 'bank/creditStatement/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def credit_statement_detail(request, id):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param id: Код типа вклада.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
    credit_statement_item = get_object_or_404(CreditStatement, id=id)
    context = {
        'credit_statement_item': credit_statement_item,
    }
    return render(request, 'bank/creditStatement/detail.html', context)

class PayrollListView(ListView):
    queryset = Payroll.objects.all()
    context_object_name = 'payroll'
    paginate_by = 25
    template_name = 'bank/payroll/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def payroll_detail(request, id):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param id: Код типа вклада.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
    payroll_item = get_object_or_404(Payroll, id=id)
    context = {
        'payroll_item': payroll_item,
    }
    return render(request, 'bank/payroll/detail.html', context)


def search_clients(request):
    if request.method == 'POST':
        query = request.POST.get('search_query')
        clients = Clients.objects.filter(Q(passport_serial_number__icontains=query))
        context = {'clients': clients}
        return render(request, 'bank/SQL-questions/clientsSearch.html', context)
    else:
        return render(request, 'bank/clients/list.html')


def delete_clients(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')

        # Удаляем записи из базы данных
        Clients.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})


# def delete_clients(request):
#     if request.method == 'POST':
#         client_id = request.POST.get('id')
#
#         if client_id:
#             try:
#                 # Удаляем запись из базы данных
#                 client = Clients.objects.get(pk=client_id)
#                 client.delete()
#
#                 return JsonResponse({'success': True})
#             except Clients.DoesNotExist:
#                 return JsonResponse({'error': f'Клиента с идентификатором {client_id} не существует.'}, status=404)
#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#         else:
#             return JsonResponse({'error': 'Не передан идентификатор клиента.'}, status=400)