# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, LoanTypes, Payroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json




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
        # Получение списка идентификаторов из POST-запроса
        ids_json = request.POST.get('ids', None)

        # Преобразование JSON-строки в список идентификаторов
        if ids_json:
            try:
                ids = json.loads(ids_json)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Ошибка декодирования JSON'})
        else:
            return JsonResponse({'success': False, 'message': 'Не найдены идентификаторы для удаления'})

        # Удаление записей из базы данных
        Clients.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})

def delete_credit_type(request):
    if request.method == 'POST':
        # Получение списка идентификаторов из POST-запроса
        ids_json = request.POST.get('ids', None)

        # Преобразование JSON-строки в список идентификаторов
        if ids_json:
            try:
                ids = json.loads(ids_json)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Ошибка декодирования JSON'})
        else:
            return JsonResponse({'success': False, 'message': 'Не найдены идентификаторы для удаления'})

        # Удаление записей из базы данных
        LoanTypes.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})

def delete_credit_statement(request):
    if request.method == 'POST':
        # Получение списка идентификаторов из POST-запроса
        ids_json = request.POST.get('ids', None)

        # Преобразование JSON-строки в список идентификаторов
        if ids_json:
            try:
                ids = json.loads(ids_json)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Ошибка декодирования JSON'})
        else:
            return JsonResponse({'success': False, 'message': 'Не найдены идентификаторы для удаления'})

        # Удаление записей из базы данных
        CreditStatement.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})


def delete_payroll(request):
    if request.method == 'POST':
        # Получение списка идентификаторов из POST-запроса
        ids_json = request.POST.get('ids', None)

        # Преобразование JSON-строки в список идентификаторов
        if ids_json:
            try:
                ids = json.loads(ids_json)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Ошибка декодирования JSON'})
        else:
            return JsonResponse({'success': False, 'message': 'Не найдены идентификаторы для удаления'})

        # Удаление записей из базы данных
        Payroll.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})

def update_client_view(request):
    if request.method == 'POST':
        # Получаем данные
        client_id = request.POST.get('client_id')
        passport = request.POST.get('my_field_passport')
        surname = request.POST.get('my_field_surname')
        name = request.POST.get('my_field_name')
        patronymic = request.POST.get('my_field_patronymic')
        address = request.POST.get('my_field_adress')
        phone_number = request.POST.get('my_field_phone')
        age = request.POST.get('my_field_age')
        sex = request.POST.get('my_field_sex')
        flag_own_car = request.POST.get('my_field_flag_own_car')
        flag_own_property = request.POST.get('my_flag_own_property')
        month_income = request.POST.get('my_field_month_income')
        count_children = request.POST.get('my_field_count_children')
        education_type = request.POST.get('my_field_education_type')

        try:
            client = Clients.objects.get(pk=client_id)
            # Обновляем поля
            client.passport_serial_number = passport
            client.surname = surname
            client.name = name
            client.patronymic = patronymic
            client.address = address
            client.phone_number = phone_number
            client.age = age
            client.sex = sex
            client.flag_own_car = 1 if flag_own_car == 'Да' else 0
            client.flag_own_property = 1 if flag_own_property == 'Да' else 0
            client.month_income = month_income
            client.count_children = count_children
            client.education_type = education_type
            client.save()
            return JsonResponse({'success': True})

        except Clients.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Клиент {client_id} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # return render(request, 'your_template.html', {})

