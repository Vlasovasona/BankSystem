# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ
import math
from datetime import date
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, LoanTypes, Payroll, AuthUser
from django.views.generic import ListView
from django.db.models import Q
from django.http import JsonResponse
import json
from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.tables import LongTable
from django.http import FileResponse, HttpResponse
import os
import tempfile
import seaborn as sb
from reportlab.platypus import Image
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import pandas as pd
from datetime import datetime

import joblib
from django.conf import settings

import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

MODEL_FILEPATH = os.path.join(settings.BASE_DIR, 'bank','static', 'bank', 'datasets', 'final_model.joblib')

class ClientListView(ListView):
    queryset = Clients.objects.order_by('id')
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
    queryset = LoanTypes.objects.order_by('id')
    context_object_name = 'credit_types'
    paginate_by = 25
    template_name = 'bank/creditTypes/list.html'

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
    queryset = CreditStatement.objects.order_by('id')
    context_object_name = 'credit_statement'
    paginate_by = 25
    template_name = 'bank/creditStatement/list.html'

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
    queryset = Payroll.objects.order_by('id')
    context_object_name = 'payroll'
    paginate_by = 25
    template_name = 'bank/payroll/list.html'

def payroll_detail(request, id):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param id: Код типа вклада.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа вклада. """
    pay = get_object_or_404(Payroll, id=id)
    context = {
        'pay': pay,
    }
    return render(request, 'bank/payroll/detail.html', context)

def client_add_detail(request):
    """Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    return render(request, 'bank/clients/add_detail.html')

def credit_types_add_detail(request):
    """Представление подробной информации о конкретном типе кредита.
    :param request: HTTP-запрос.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали типа кредита. """
    return render(request, 'bank/creditTypes/add_detail.html')

def credit_statement_add_detail(request):
    """Представление подробной информации о конкретном кредитном договоре.
    :param request: HTTP-запрос.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали кредитного договора. """
    return render(request, 'bank/creditStatement/add_detail.html')

def payroll_add_detail(request):
    """Представление подробной информации о конкретном платеже.
    :param request: HTTP-запрос.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали платежа. """
    return render(request, 'bank/payroll/add_detail.html')

def search_clients(request):
    """Использование поисковой строки для поиска клиента по паспортным данным.
        :param request: HTTP-запрос.
        :return: Возвращает HTML-шаблон с контекстом, содержащим найденного клиента. """
    if request.method == 'POST':
        query = request.POST.get('search_query')
        clients = Clients.objects.filter(Q(passport_serial_number__icontains=query))
        context = {'clients': clients}
        return render(request, 'bank/SQL-questions/clientsSearch.html', context)
    else:
        return render(request, 'bank/clients/list.html')

def delete_clients(request):
    """Осуществление удаления списка клиентов у которых активирован чекбокс."""
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

def delete_single_client(request):
    if request.method == 'POST':
        # Десериализация JSON тела запроса
        try:
            data = json.loads(request.body)
            client_id = data.get('client_id')  # Теперь получаем client_id из десериализованных данных
        except json.JSONDecodeError:
            return JsonResponse({'error': "Ошибка разбора JSON."}, status=400)

        if client_id is not None:
            try:
                client = Clients.objects.get(id=int(client_id))
                client.delete()
                return JsonResponse({'success': True}, status=200)
            except Clients.DoesNotExist:
                return JsonResponse({'error': f"Клиента с ID {client_id} не существует."}, status=404)
            except ValueError:
                return JsonResponse({'error': f"Передано неверное значение ID: {client_id}."}, status=400)
        else:
            return JsonResponse({'error': "Не найден параметр 'client_id'."}, status=400)
    return JsonResponse({}, status=405)

def delete_single_statement(request):
    if request.method == 'POST':
        # Десериализация JSON тела запроса
        try:
            data = json.loads(request.body)
            credit_state_id = data.get('credit_state_id')  # Теперь получаем client_id из десериализованных данных
        except json.JSONDecodeError:
            return JsonResponse({'error': "Ошибка разбора JSON."}, status=400)

        if credit_state_id is not None:
            try:
                state = CreditStatement.objects.get(id=int(credit_state_id))
                state.delete()
                return JsonResponse({'success': True}, status=200)
            except CreditStatement.DoesNotExist:
                return JsonResponse({'error': f"Договора с ID {credit_state_id} не существует."}, status=404)
            except ValueError:
                return JsonResponse({'error': f"Передано неверное значение ID: {credit_state_id}."}, status=400)
        else:
            return JsonResponse({'error': "Не найден параметр 'credit_state_id'."}, status=400)
    return JsonResponse({}, status=405)

def delete_single_loan_type(request):
    if request.method == 'POST':
        # Десериализация JSON тела запроса
        try:
            data = json.loads(request.body)
            loan_type_id = data.get('credit_type_id')  # Теперь получаем client_id из десериализованных данных
        except json.JSONDecodeError:
            return JsonResponse({'error': "Ошибка разбора JSON."}, status=400)

        if loan_type_id is not None:
            try:
                type = LoanTypes.objects.get(id=int(loan_type_id))
                type.delete()
                return JsonResponse({'success': True}, status=200)
            except LoanTypes.DoesNotExist:
                return JsonResponse({'error': f"Договора с ID {loan_type_id} не существует."}, status=404)
            except ValueError:
                return JsonResponse({'error': f"Передано неверное значение ID: {loan_type_id}."}, status=400)
        else:
            return JsonResponse({'error': "Не найден параметр 'loan_type_id'."}, status=400)
    return JsonResponse({}, status=405)

def delete_single_payroll(request):
    if request.method == 'POST':
        # Десериализация JSON тела запроса
        try:
            data = json.loads(request.body)
            pay_id = data.get('pay_id')  # Теперь получаем client_id из десериализованных данных
        except json.JSONDecodeError:
            return JsonResponse({'error': "Ошибка разбора JSON."}, status=400)

        if pay_id is not None:
            try:
                pay = Payroll.objects.get(id=int(pay_id))
                pay.delete()
                return JsonResponse({'success': True}, status=200)
            except Payroll.DoesNotExist:
                return JsonResponse({'error': f"Платежа с ID {pay_id} не существует."}, status=404)
            except ValueError:
                return JsonResponse({'error': f"Передано неверное значение ID: {pay_id}."}, status=400)
        else:
            return JsonResponse({'error': "Не найден параметр 'pay_id'."}, status=400)
    return JsonResponse({}, status=405)

def delete_credit_type(request):
    """Осуществление удаления списка типов кредита у которых активирован чекбокс."""
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
    """Осуществление удаления списка кредитных договоров у которых активирован чекбокс."""
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
    """Осуществление удаления списка платежей у которых активирован чекбокс."""
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
    """Осуществление изменение клиента в БД."""
    if request.method == 'POST':
        # Получаем данные
        client_id = request.POST.get('client_id')

        errors = {}
        # Валидируем каждое поле
        passport = request.POST.get('my_field_passport')
        if not re.match(r'\d{10}', passport):
            errors['passport'] = 'Серия и номер паспорта'

        surname = request.POST.get('my_field_surname')
        if not re.match(r'^[А-ЯЁа-яё ]+$', surname):
            errors['surname'] = 'Фамилия может состоять только из русских букв!'

        name = request.POST.get('my_field_name')
        if not re.match(r'^[А-ЯЁа-яё ]+$', name):
            errors['name'] = 'Имя может состоять только из русских букв!'

        patronymic = request.POST.get('my_field_patronymic')
        if not re.match(r'^[А-ЯЁа-яё ]+$', patronymic):
            errors['patronymic'] = 'Отчество может состоять только из русских букв!'

        adress = request.POST.get('my_field_adress')

        phone_number = request.POST.get('my_field_phone')
        if not re.match(r'^8[0-9]{10}$', phone_number):
            errors['phone'] = 'Номер телефона должен начинаться с 8 и состоять из 11 цифр'

        age = request.POST.get('my_field_age')
        if not isinstance(age, str):
            errors['age'] = 'Поле возраста должно содержать строку.'
        elif not age.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['age'] = 'Возраст должен быть числовым значением.'
        else:
            # Преобразуем возраст в целое число
            age_int = int(age)

            # Проверяем диапазон допустимых значений
            if not (18 <= age_int < 100):
                errors['age'] = 'Возраст должен быть целым числом от 18 до 99.'

        sex = request.POST.get('my_field_sex')
        if not isinstance(sex, str):
            errors['sex'] = 'Обязательно для заполнения.'
        if not (sex == 'Мужской' or sex == 'Женский'):
            errors['sex'] = 'Допустимы только значения Мужской/Женский'

        flag_own_car = request.POST.get('my_field_flag_own_car')
        if not isinstance(flag_own_car, str):
            errors['car'] = 'Обязательно для заполнения.'
        if not (flag_own_car == 'Да' or flag_own_car == 'Нет'):
            errors['car'] = 'Допустимы только значения Да/Нет'

        flag_own_property = request.POST.get('my_flag_own_property')
        if not isinstance(flag_own_property, str):
            errors['property'] = 'Обязательно для заполнения.'
        if not (flag_own_property == 'Да' or flag_own_property == 'Нет'):
            errors['property'] = 'Допустимы только значения Да/Нет'

        month_income = request.POST.get('my_field_month_income')
        if not isinstance(month_income, str):
            errors['income'] = 'Обязательно для заполнения.'
        elif not month_income.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['income'] = 'Доход должен быть целым положительным числом.'

        count_children = request.POST.get('my_field_count_children')
        if not isinstance(count_children, str):
            errors['children'] = 'Обязательно для заполнения.'
        elif not count_children.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['children'] = 'Количество детей должно быть целым неотрицательным числом.'

        education_type = request.POST.get('my_field_education_type')
        if not isinstance(education_type, str):
            errors['education'] = 'Обязательно для заполнения.'
        if not (education_type == 'Высшее' or education_type == 'Среднее специальное'):
            errors['education'] = 'Допустимы только значения Высшее/Среднее специальное'

        if errors:
            return JsonResponse({'errors': errors})

        try:
            client = Clients.objects.get(pk=client_id)
            # Обновляем поля
            client.passport_serial_number = passport
            client.surname = surname
            client.name = name
            client.patronymic = patronymic
            client.address = adress
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

def update_loan_type(request):
    """Осуществление изменение типа кредита в БД."""
    if request.method == 'POST':
        # Получаем данные
        credit_type_id = request.POST.get('credit_type_id')
        errors = {}
        registration_number = request.POST.get('my_field_credit_type_code')
        if not isinstance(registration_number, str):
            errors['credit_types'] = 'Регистрационный номер обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not registration_number.isdigit() or int(registration_number) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['credit_types'] = 'Ргеистрационный номер должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        name_of_the_type = request.POST.get('my_field_credit_type_name')
        if not isinstance(name_of_the_type, str):
            errors['name'] = 'Название типа кредита обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})

        interest_rate = request.POST.get('my_field_credit_percent')
        if not isinstance(interest_rate, str):
            errors['percent'] = 'Поле обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not is_positive_number(interest_rate):
            errors['percent'] = 'Процентная ставка должна быть положительным числом.'
            return JsonResponse({'success': False, 'errors': errors})

        try:
            credit_type = LoanTypes.objects.get(pk=credit_type_id)
            # Обновляем поля
            credit_type.registration_number = registration_number
            credit_type.name_of_the_type = name_of_the_type
            credit_type.interest_rate = interest_rate
            credit_type.save()
            return JsonResponse({'success': True})

        except LoanTypes.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Тип кредита {credit_type_id} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def update_payroll(request):
    """Осуществление изменение платежа в БД."""
    if request.method == 'POST':
        # Получаем данные
        pay_id = request.POST.get('pay_id')
        errors = {}
        loan_id = request.POST.get('my_field_loan')
        if not isinstance(loan_id, str):
            errors['loan'] = 'Номер договора обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not loan_id.isdigit() or int(loan_id) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['loan'] = 'Номер договора должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        payment_date = request.POST.get('my_field_payment_date')
        date_pattern = r'^([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'

        match = re.match(date_pattern, payment_date)
        if not isinstance(payment_date, str) or not match:
            errors['date'] = 'Дата должна быть в формате ГГГГ-ММ-ДД'
            return JsonResponse({'success': False, 'errors': errors})
        else:
            year, month, day = map(int, match.groups())
            # Дополнительная проверка диапазона года: от 1950 до 2025 включительно
            if not (1950 <= year <= 2025):
                errors['date'] = f'Год должен быть между 1950 и 2025, введён {year}'
                return JsonResponse({'success': False, 'errors': errors})
            # Проверка корректности месяца (от 1 до 12)
            if not (1 <= month <= 12):
                errors['date'] = f'Месяц должен быть между 1 и 12, введён {month}'
                return JsonResponse({'success': False, 'errors': errors})
            # Проверка корректности дня (от 1 до 31)
            if not (1 <= day <= 31):
                errors['date'] = f'День должен быть между 1 и 31, введён {day}'
                return JsonResponse({'success': False, 'errors': errors})

        payment_status = request.POST.get('my_field_payment_status')
        if not isinstance(payment_status, str):
            errors['status'] = 'Обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        if not (payment_status == 'X' or payment_status == 'C' or (payment_status.isdigit() and 0<=int(payment_status)<=5)):
            errors['status'] = 'Допустимы только значения X, C или число от 0 до 5'
            return JsonResponse({'success': False, 'errors': errors})

        try:
            # Попытка получения объекта CreditStatement
            loan = CreditStatement.objects.get(number_of_the_loan_agreement=loan_id)
        except CreditStatement.DoesNotExist:
            errors['loan'] = f'Запись в ведомости с номером договора {loan_id} не найдена.'
            return JsonResponse({'success': False, 'errors': errors})

        try:
            # Попытка получения объекта CreditStatement
            loan = CreditStatement.objects.get(number_of_the_loan_agreement=loan_id)
        except CreditStatement.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Запись в ведомости с номером договора {loan_id} не найдена.'
            })

        try:
            pay = Payroll.objects.get(pk=pay_id)
            # Обновляем поля
            pay.loan = loan
            pay.payment_date = payment_date
            pay.payment_status = payment_status
            pay.save()
            return JsonResponse({'success': True})

        except Payroll.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Платеж {pay_id} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def update_credit_statement(request):
    """Осуществление изменение кредитного договора в БД."""
    if request.method == 'POST':

        errors = {}
        statement_id = request.POST.get('credit_state_id')

        number_of_the_loan_agreement = request.POST.get('my_field_number_of_the_loan_agreement')
        if not isinstance(number_of_the_loan_agreement, str):
            errors['number'] = 'Номер кредитного договора обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not number_of_the_loan_agreement.isdigit() or int(number_of_the_loan_agreement) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['number'] = 'Номер кредитного договора должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        credit_amount = request.POST.get('my_field_credit_amount')
        if not isinstance(credit_amount, str):
            errors['amount'] = 'Сумма кредита обязательная для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not credit_amount.isdigit() or int(credit_amount) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['amount'] = 'Сумма кредита должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        term_month = request.POST.get('my_term_month')
        if not isinstance(term_month, str):
            errors['month'] = 'Длительность выплат обязательна для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not term_month.isdigit() or int(term_month) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['month'] = 'Длительность выплат должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        loan_type = request.POST.get('my_field_loan_type')
        if not isinstance(loan_type, str):
            errors['loanType'] = 'Регистр. номер типа кредита обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not loan_type.isdigit() or int(loan_type) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['loanType'] = 'Регистр. номер типа кредита должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        client_passport = request.POST.get('my_field_client')
        if not isinstance(client_passport, str):
            errors['client'] = 'Паспорт клиента обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not client_passport.isdigit() or int(client_passport) <= 0 or not re.match(r'\d{10}', client_passport):
            # Если введено не число, сообщаем об ошибке
            errors['client'] = 'Серия и номер паспорта должны быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})


        if 'loanType' not in errors:
            try:
                # Попытка получения объекта LoanType
                loan_t = LoanTypes.objects.get(registration_number=int(loan_type))
            except LoanTypes.DoesNotExist:
                errors['loanType'] = f'Тип кредита с регистрационным номером {loan_type} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if 'client' not in errors:
            try:
                # Попытка получения объекта Client
                client = Clients.objects.get(passport_serial_number=int(client_passport))
            except Clients.DoesNotExist:
                errors['client'] = f'Клиент с паспортными данными {client_passport} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if errors:
            return JsonResponse({'errors': errors})

        try:
            statement = CreditStatement.objects.get(pk=statement_id)
            # Обновляем поля

            percent = loan_t.interest_rate
            count_of_pays = Payroll.objects.filter(loan=CreditStatement.objects.get(pk=statement_id)).count()
            old_payment = (CreditStatement.objects.get(pk=statement_id)).monthly_payment

            if statement.repayment_status != 1:
                balance_of_debt = (int(statement.credit_amount) - int(old_payment) * count_of_pays) * (
                            percent / 100 + 1.0) / int(term_month)
                if balance_of_debt <= 0:
                    statement.repayment_status = 1
                else:
                    statement.monthly_payment = math.ceil(balance_of_debt)

            statement.number_of_the_loan_agreement = number_of_the_loan_agreement
            statement.credit_amount = credit_amount
            statement.term_month = term_month
            statement.loan_type = loan_t
            statement.client = client
            statement.save()
            return JsonResponse({'success': True})

        except CreditStatement.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Кредитный договор {statement_id} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_client(request):
    """Осуществление добавления клиента в БД."""
    if request.method == 'POST':
        # Получаем данные

        errors = {}
        # Валидируем каждое поле
        passport = request.POST.get('my_field_passport')
        if not re.match(r'\d{10}', passport):
            errors['passport'] = 'Серия и номер паспорта должна состоять из 10 цифр'

        surname = request.POST.get('my_field_surname')
        if not re.match(r'^[А-ЯЁа-яё ]+$', surname):
            errors['surname'] = 'Фамилия может состоять только из русских букв!'

        name = request.POST.get('my_field_name')
        if not re.match(r'^[А-ЯЁа-яё ]+$', name):
            errors['name'] = 'Имя может состоять только из русских букв!'

        patronymic = request.POST.get('my_field_patronymic')
        if not re.match(r'^[А-ЯЁа-яё ]+$', patronymic):
            errors['patronymic'] = 'Отчество может состоять только из русских букв!'

        adress = request.POST.get('my_field_adress')

        phone_number = request.POST.get('my_field_phone')
        if not re.match(r'^8[0-9]{10}$', phone_number):
            errors['phone'] = 'Номер телефона должен начинаться с 8 и состоять из 11 цифр'

        age = request.POST.get('my_field_age')
        if not isinstance(age, str):
            errors['age'] = 'Поле возраста должно содержать строку.'
        elif not age.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['age'] = 'Возраст должен быть числовым значением.'
        else:
            # Преобразуем возраст в целое число
            age_int = int(age)

            # Проверяем диапазон допустимых значений
            if not (18 <= age_int < 100):
                errors['age'] = 'Возраст должен быть целым числом от 18 до 99.'

        sex = request.POST.get('my_field_sex')
        if not isinstance(sex, str):
            errors['sex'] = 'Обязательно для заполнения.'
        if not (sex == 'Мужской' or sex == 'Женский'):
            errors['sex'] = 'Допустимы только значения Мужской/Женский'

        flag_own_car = request.POST.get('my_field_flag_own_car')
        if not isinstance(flag_own_car, str):
            errors['car'] = 'Обязательно для заполнения.'
        if not (flag_own_car == 'Да' or flag_own_car == 'Нет'):
            errors['car'] = 'Допустимы только значения Да/Нет'

        flag_own_property = request.POST.get('my_flag_own_property')
        if not isinstance(flag_own_property, str):
            errors['property'] = 'Обязательно для заполнения.'
        if not (flag_own_property == 'Да' or flag_own_property == 'Нет'):
            errors['property'] = 'Допустимы только значения Да/Нет'

        month_income = request.POST.get('my_field_month_income')
        if not isinstance(month_income, str):
            errors['income'] = 'Обязательно для заполнения.'
        elif not month_income.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['income'] = 'Доход должен быть целым положительным числом.'

        count_children = request.POST.get('my_field_count_children')
        if not isinstance(count_children, str):
            errors['children'] = 'Обязательно для заполнения.'
        elif not count_children.isdigit():
            # Если введено не число, сообщаем об ошибке
            errors['children'] = 'Количество детей должно быть целым неотрицательным числом.'

        education_type = request.POST.get('my_field_education_type')
        if not isinstance(education_type, str):
            errors['education'] = 'Обязательно для заполнения.'
        if not (education_type == 'Высшее' or education_type == 'Среднее специальное'):
            errors['education'] = 'Допустимы только значения Высшее/Среднее специальное'


        if re.match(r'\d{10}', passport) and Clients.objects.filter(passport_serial_number=passport).exists():
            errors['passport'] = 'Клиент с такими паспортными данными существует!'
        if errors:
            return JsonResponse({'errors': errors})
        try:
            # Создаем нового клиента
            client = Clients(
                passport_serial_number=passport,
                surname=surname,
                name=name,
                patronymic=patronymic,
                adress=adress,
                phone_number=phone_number,
                age=age,
                sex=sex,
                flag_own_car=1 if flag_own_car == 'Да' else 0,
                flag_own_property=1 if flag_own_property == 'Да' else 0,
                month_income=month_income,
                count_children=count_children,
                education_type=education_type
            )
            client.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def is_positive_number(value):
    try:
        float_value = float(value)
        if float_value > 0:
            return True
        else:
            return False
    except ValueError:
        return False

def add_new_loan_type(request):
    """Осуществление добавления типа кредита в БД."""
    if request.method == 'POST':
        # Получаем данные
        errors = {}
        registration_number = request.POST.get('my_field_credit_type_code')
        if not isinstance(registration_number, str):
            errors['credit_types'] = 'Регистрационный номер обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not registration_number.isdigit() or int(registration_number) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['credit_types'] = 'Ргеистрационный номер должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        name_of_the_type = request.POST.get('my_field_credit_type_name')
        if not isinstance(name_of_the_type, str):
            errors['name'] = 'Название типа кредита обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})

        interest_rate = request.POST.get('my_field_credit_percent')
        if not isinstance(interest_rate, str):
            errors['percent'] = 'Поле обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not is_positive_number(interest_rate):
            errors['percent'] = 'Процентная ставка должна быть положительным числом.'
            return JsonResponse({'success': False, 'errors': errors})

        if 'credit_types' not in errors:
            if LoanTypes.objects.filter(registration_number=registration_number).exists():
                errors['credit_types'] = "Тип кредита с таким регистрационным номером уже существует"
                return JsonResponse({'success': False, 'errors': errors})

        try:
            credit_type = LoanTypes(
                registration_number = registration_number,
                name_of_the_type = name_of_the_type,
                interest_rate = interest_rate
            )
            credit_type.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_payroll(request):
    """Осуществление добавления платежа в БД."""
    if request.method == 'POST':
        # Получаем данные
        errors = {}
        loan_id = request.POST.get('my_field_loan')
        if not isinstance(loan_id, str):
            errors['loan'] = 'Номер договора обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not loan_id.isdigit() or int(loan_id) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['loan'] = 'Номер договора должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        payment_date = request.POST.get('my_field_payment_date')
        date_pattern = r'^([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'

        match = re.match(date_pattern, payment_date)
        if not isinstance(payment_date, str) or not match:
            errors['date'] = 'Дата должна быть в формате ГГГГ-ММ-ДД'
            return JsonResponse({'success': False, 'errors': errors})
        else:
            year, month, day = map(int, match.groups())
            # Дополнительная проверка диапазона года: от 1950 до 2025 включительно
            if not (1950 <= year <= 2025):
                errors['date'] = f'Год должен быть между 1950 и 2025, введён {year}'
                return JsonResponse({'success': False, 'errors': errors})
            # Проверка корректности месяца (от 1 до 12)
            if not (1 <= month <= 12):
                errors['date'] = f'Месяц должен быть между 1 и 12, введён {month}'
                return JsonResponse({'success': False, 'errors': errors})
            # Проверка корректности дня (от 1 до 31)
            if not (1 <= day <= 31):
                errors['date'] = f'День должен быть между 1 и 31, введён {day}'
                return JsonResponse({'success': False, 'errors': errors})

        payment_status = request.POST.get('my_field_payment_status')
        if not isinstance(payment_status, str):
            errors['status'] = 'Обязательно для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        if not (payment_status == 'X' or payment_status == 'C' or (
                payment_status.isdigit() and 0 <= int(payment_status) <= 5)):
            errors['status'] = 'Допустимы только значения X, C или число от 0 до 5'
            return JsonResponse({'success': False, 'errors': errors})


        try:
            # Попытка получения объекта CreditStatement
            loan = CreditStatement.objects.get(number_of_the_loan_agreement=loan_id)
            if Payroll.objects.filter(loan=loan, payment_date=payment_date).exists():
                errors['date'] = "Для этого кредита в эту дату уже был внесен платеж!"
                return JsonResponse({'success': False, 'errors': errors})
        except CreditStatement.DoesNotExist:
            errors['loan'] = 'Запись с таким номером договора не найдена'
            return JsonResponse({'success': False, 'errors': errors})

        try:
            current_loan_pays = Payroll.objects.filter(loan=loan).latest('payment_date')
            last_data = current_loan_pays.payment_date
            create_data = loan.loan_opening_date
            new_data = datetime.strptime(payment_date, '%Y-%m-%d').date()

            # Извлекаем отдельные компоненты (день, месяц, год)
            dd_new = new_data.day
            mm_new = new_data.month
            yy_new = new_data.year

            dd_create = create_data.day
            mm_create = create_data.month
            yy_create = create_data.year

            dd_last = last_data.day
            mm_last = last_data.month
            yy_last = last_data.year

            # Проверяем условия:
            if dd_new == dd_create and mm_last + 1 == mm_new and yy_new == yy_last:
                payment_status = 'C'
            elif mm_last == mm_new and yy_new == yy_last:
                return JsonResponse({'success': False, 'error': 'По этому кредиту уже была выплата в этом месяце'})
            else:
                # Находим разницу между датами
                delta = abs((new_data - last_data).days)
                if 1 <= delta <= 29: payment_status = '0'
                elif 30 <= delta <= 59: payment_status = '1'
                elif 60 <= delta <= 89: payment_status = '2'
                elif 90 <= delta <= 119: payment_status = '3'
                elif 120 <= delta <= 149: payment_status = '4'
                else: payment_status = '5'

            pay = Payroll(
                loan = loan,
                payment_date = payment_date,
                payment_status = payment_status
            )
            pay.save()

            count_of_pays = Payroll.objects.filter(loan=loan).count()
            # автоматически считать статус погашения кредита для которого внесен новый платеж
            if loan.term_month == count_of_pays:
                loan.repayment_status = 1
                loan.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_credit_statement(request):
    """Осуществление добавления кредитного договора в БД."""
    if request.method == 'POST':
        # Получаем данные
        errors = {}
        number_of_the_loan_agreement = request.POST.get('my_field_number_of_the_loan_agreement')
        if not isinstance(number_of_the_loan_agreement, str):
            errors['number'] = 'Номер кредитного договора обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not number_of_the_loan_agreement.isdigit() or int(number_of_the_loan_agreement) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['number'] = 'Номер кредитного договора должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        credit_amount = request.POST.get('my_field_credit_amount')
        if not isinstance(credit_amount, str):
            errors['amount'] = 'Сумма кредита обязательная для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not credit_amount.isdigit() or int(credit_amount) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['amount'] = 'Сумма кредита должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        term_month = request.POST.get('my_term_month')
        if not isinstance(term_month, str):
            errors['month'] = 'Длительность выплат обязательна для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not term_month.isdigit() or int(term_month) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['month'] = 'Длительность выплат должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        loan_type = request.POST.get('my_field_loan_type')
        if not isinstance(loan_type, str):
            errors['loanType'] = 'Регистр. номер типа кредита обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not loan_type.isdigit() or int(loan_type) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['loanType'] = 'Регистр. номер типа кредита должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        client_passport = request.POST.get('my_field_client')
        if not isinstance(client_passport, str):
            errors['client'] = 'Паспорт клиента обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not client_passport.isdigit() or int(client_passport) <= 0 or not re.match(r'\d{10}', client_passport):
            # Если введено не число, сообщаем об ошибке
            errors['client'] = 'Серия и номер паспорта должны быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        if 'number' not in errors:
            if CreditStatement.objects.filter(number_of_the_loan_agreement=int(number_of_the_loan_agreement)).exists():
                errors['number'] = "Кредит с таким номером договора уже существует"
                return JsonResponse({'success': False, 'errors': errors})

        if 'loanType' not in errors:
            try:
                # Попытка получения объекта LoanType
                loan_t = LoanTypes.objects.get(registration_number=int(loan_type))
            except LoanTypes.DoesNotExist:
                errors['loanType'] = f'Тип кредита с регистрационным номером {loan_type} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if 'client' not in errors:
            try:
                # Попытка получения объекта Client
                client = Clients.objects.get(passport_serial_number=int(client_passport))
            except Clients.DoesNotExist:
                errors['client'] = f'Клиент с паспортными данными {client_passport} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        try:
            percent = loan_t.interest_rate
            monthly_payment = math.ceil((int(credit_amount)*(percent/100+1.0))/int(term_month))

            today = date.today()
            formatted_date = today.strftime('%Y-%m-%d')

            statement = CreditStatement(
                number_of_the_loan_agreement = number_of_the_loan_agreement,
                credit_amount = credit_amount,
                term_month = term_month,
                monthly_payment = monthly_payment,
                loan_opening_date = formatted_date,
                repayment_status = 0,
                loan_type = loan_t,
                client = client
            )
            statement.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_user(request):
    """Осуществление регистрации нового юзера."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняет нового пользователя с указанным email и статусом staff
            login(request, user)
            return redirect('/bank/personal_account/')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'bank/registrationPage.html', context)

def register_view(request):
    """Осуществление регистрации нового юзера."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняет нового пользователя с указанным email и статусом staff
            return redirect('/bank/personal_account/')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'bank/registrationPage.html', context)

def login_view(request):
    """Осуществление авторизации юзера."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/bank/clients/')  # Переадресация после успешного входа
        else:
            print("Ошибка при входе")
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'bank/login_start_page.html', context)

def logout_view(request):
    """Осуществление выхода из аккаунта текущего юзера."""
    logout(request)
    return redirect('home')

def personal_account(request):
    """Осуществление перехода в ЛК с автоматическим определением прав юзера."""
    context = {
        'user': request.user
    }
    if request.user.is_staff == 1:
        return render(request, 'bank/accounts/admin_account.html', context)
    else:
        return render(request, 'bank/accounts/regular.html', context)

def delete_users(request):
    """Осуществление удаления списка юзеров у которых активирован чекбокс."""
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
        AuthUser.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True})

class UsersListView(ListView):
    queryset = AuthUser.objects.all()
    context_object_name = 'users'
    paginate_by = 10
    template_name = 'bank/accounts/admin_capabilities/users_list.html'

def user_detail(request, username):
    user = get_object_or_404(AuthUser, username=username)
    context = {
        'user': user,
    }
    return render(request, 'bank/accounts/admin_capabilities/users_detail.html', context)

def update_user(request):
    """Осуществление изменение платежа в БД."""
    if request.method == 'POST':
        # Получаем данные
        username = request.POST.get('my_field_login')
        first_name = request.POST.get('my_field_name')
        last_name = request.POST.get('my_field_last_name')
        email = request.POST.get('my_field_email')
        is_staff = request.POST.get('my_field_is_staff')
        is_active = request.POST.get('my_field_is_active')

        try:
            user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Пользователь с логином {username} не найден.'
            })

        try:
            user = AuthUser.objects.get(username=username)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_staff = 1 if is_staff == "Да" else 0
            user.is_active = 1 if is_active == "Да" else 0
            user.save()
            return JsonResponse({'success': True})

        except Payroll.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Пользователь {username} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def delete_single_user(request):
    if request.method == 'POST':
        # Десериализация JSON тела запроса
        try:
            data = json.loads(request.body)
            username = data.get('my_field_login')  # Теперь получаем client_id из десериализованных данных
        except json.JSONDecodeError:
            return JsonResponse({'error': "Ошибка разбора JSON."}, status=400)

        if username is not None:
            try:
                user = AuthUser.objects.get(username=username)
                user.delete()
                return JsonResponse({'success': True}, status=200)
            except AuthUser.DoesNotExist:
                return JsonResponse({'error': f"Пользователя с ID {username} не существует."}, status=404)
            except ValueError:
                return JsonResponse({'error': f"Передано неверное значение ID: {username}."}, status=400)
        else:
            return JsonResponse({'error': "Не найден параметр 'username'."}, status=400)
    return JsonResponse({}, status=405)

# отчеты
def show_reports_main_page(request):
    return render(request, 'bank/left_menu/reports/report_main_page.html')


def create_report(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_tables = data.get('tables', [])

        try:
            # Создание временного файла для хранения PDF
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_filename = temp_file.name
                pdfmetrics.registerFont(
                    TTFont('Arial',
                           'C:/Users/sofav/PycharmProjects/PythonProject/mysite/bank/static/bank/fonts/arial3.ttf'))

                styles = getSampleStyleSheet()

                # Обновление существующего стиля 'Normal'
                styles['Normal'].fontName = 'Arial'
                styles['Normal'].fontSize = 12

                heading_style = ParagraphStyle(
                    name='TableHeading',
                    parent=styles['Normal'],
                    spaceAfter=10
                )
                doc = SimpleDocTemplate("output.pdf", pagesize=landscape(letter))

                elements = []

                for table_name in selected_tables:
                    if table_name == 'Clients':
                        clients_data = Clients.objects.all().values_list('passport_serial_number', 'name', 'surname',
                                                                         'patronymic', 'phone_number', 'age', 'sex',
                                                                         'month_income', 'count_children',
                                                                         'education_type')
                        client_table = LongTable(
                            [['Серия номер паспорта', 'Имя', 'Фамилия', 'Отчество', 'Номер телефона',
                              'Возраст', 'Пол', 'Доход в месяц', 'Кол-во детей',
                              'Образование']] + list(clients_data))

                        client_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('GRID', (0, 0), (-1, -1), 0.25, 'black'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))

                        elements.append(Paragraph(f"Таблица Клиенты", heading_style))
                        elements.append(client_table)
                    elif table_name == 'LoanTypes':
                        pay_data = LoanTypes.objects.all().values_list('registration_number', 'name_of_the_type',
                                                                       'interest_rate')
                        pay_table = LongTable(
                            [['Регистрационный номер', 'Название типа кредита', 'Процентная ставка']] + list(pay_data))
                        pay_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('GRID', (0, 0), (-1, -1), 0.25, 'black'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        elements.append(Paragraph(f"Таблица Типы кредитов", heading_style))
                        elements.append(pay_table)
                    elif table_name == 'CreditStatement':
                        state_data = CreditStatement.objects.select_related(
                            'loan_type',
                            'client'
                        ).all().values_list(
                            'number_of_the_loan_agreement',
                            'credit_amount',
                            'term_month',
                            'monthly_payment',
                            'loan_opening_date',
                            'repayment_status',
                            'loan_type__registration_number',
                            'client__passport_serial_number'
                        )
                        state_table = LongTable([['Договор', 'Сумма', 'Срок (мес.)', 'Ежемесячная выплата',
                                                  'Дата оформления', 'Статус погашения', 'Тип кредита',
                                                  'Паспорт клиента']] + list(state_data))
                        state_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('GRID', (0, 0), (-1, -1), 0.25, 'black'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]))
                        elements.append(Paragraph(f"Таблица Кредитная ведомость", heading_style))
                        elements.append(state_table)
                    elif table_name == 'Credit_structure':
                        months_dict = {
                            1: "январь",
                            2: "февраль",
                            3: "март",
                            4: "апрель",
                            5: "май",
                            6: "июнь",
                            7: "июль",
                            8: "август",
                            9: "сентябрь",
                            10: "октябрь",
                            11: "ноябрь",
                            12: "декабрь"
                        }

                        statement = get_pandas_dataset_statement()
                        loanTypes = get_pandas_dataset_types()

                        data = pd.merge(statement, loanTypes, left_on='loan_type_id', right_on='id', how='left')

                        current_year = datetime.now().year
                        current_month = datetime.now().month

                        mask = (pd.to_datetime(data['loan_opening_date']).dt.year == current_year) & \
                               (pd.to_datetime(data['loan_opening_date']).dt.month == current_month)

                        grouped_data = data[mask].groupby('loan_type_id')['credit_amount'].sum()

                        labels = data[['name_of_the_type', 'registration_number']].drop_duplicates().values

                        # Формируем подписи в формате: "Рег.номер (Название)"
                        formatted_labels = [f"{reg_num} ({name})" for reg_num, name in labels]

                        # Генерация изображения графика
                        chart_image_path = generate_chart_image('1', grouped_data, formatted_labels,
                                                               f'Структура кредитного портфеля за {months_dict[current_month]} {current_year}г.')

                        elements.append(Image(chart_image_path, width=7 * inch,
                                              height=4 * inch))

                    elif table_name == 'PaymentStatus-MonthIncome':
                        clients = get_pandas_dataset_clients()
                        statement = get_pandas_dataset_statement()
                        payment = get_pandas_dataset_payroll()

                        merged_df = pd.merge(statement, clients, left_on='client_id', right_on='id', how='left')
                        merged_df = merged_df.dropna()

                        merged_df = pd.merge(payment, merged_df, left_on='loan_id', right_on='id_x', how='left')
                        merged_df = merged_df.dropna()

                        merged_df['payment_status'] = pd.to_numeric(merged_df['payment_status'], errors='coerce')

                        # Удаление строк с NaN значениями
                        df_clean = merged_df.dropna(subset=['payment_status'])
                        mean_payment_status = df_clean.groupby('id_y')['payment_status'].mean().reset_index()
                        mean_payment_status = pd.merge(mean_payment_status, clients, left_on='id_y', right_on='id',
                                                       how='left')
                        sorted_mean_payment_status = mean_payment_status.sort_values(by=['month_income'])

                        chart_image_path = generate_chart_image('2', sorted_mean_payment_status, 'NaN',f'Зависимость среднего значения просроченного платежа от месячного дохода')

                        elements.append(Image(chart_image_path, width=7 * inch,
                                              height=4 * inch))

                    elif table_name == 'Year':
                        statement = get_pandas_dataset_statement()
                        statement['loan_opening_date'] = pd.to_datetime(statement['loan_opening_date'])
                        current_year = datetime.now().year

                        df_2025 = statement[statement['loan_opening_date'].dt.year == current_year]

                        # Группируем данные по месяцам и считаем сумму кредитов
                        grouped_data = df_2025.groupby(df_2025['loan_opening_date'].dt.month)['credit_amount'].sum()
                        
                        chart_image_path = generate_chart_image('3', grouped_data, current_year,
                                                                f'Годовой отчет о сумме выданных кредитов')

                        elements.append(Image(chart_image_path, width=7 * inch,
                                              height=4 * inch))


                doc.build(elements)

                # Отправляем созданный файл пользователю
                with open('output.pdf', 'rb') as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="output.pdf"'
                    return response
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if os.path.exists('output.pdf'):
                os.remove('output.pdf')

    return JsonResponse({'error': 'Метод не поддерживается'}, status=400)
import matplotlib
matplotlib.use('Agg')

def generate_chart_image(st, grouped_data, labels, title):
    if st == '1':
        plt.figure(figsize=(9, 6))
        # Обеспечиваем, что grouped_data и labels не пустые
        if grouped_data.empty or len(labels) == 0:
            return None
        grouped_data.plot(kind='pie', autopct='%1.1f%%', labels=labels)
        plt.title(title)
        plt.ylabel('')
    elif st == '2':
        plt.figure(figsize=(12, 8))
        plt.scatter(grouped_data['month_income'], grouped_data['payment_status'],
                    label='Статус платежа/доход в месяц')
        plt.xlabel('Месячный доход')
        plt.ylabel('Среднее значение просрочки')
        plt.title(title)
        plt.legend()
        plt.grid(True)
    elif st == '3':
        median_value = grouped_data.median()

        # Построение столбчатой диаграммы
        plt.figure(figsize=(10, 6))

        for i, value in enumerate(grouped_data):
            if value < median_value:  # Если значение меньше медианы, красим столбец в красный цвет
                color = 'red'
            else:
                color = 'SlateBlue'

            plt.bar(i + 1, value / 1_000_000, color=color)  # Используем индекс для обозначения месяца

        plt.xlabel(f'Месяцы {labels} года')
        plt.ylabel('Сумма оформленных кредитов (млн.р.)')
        plt.title('Годовой отчет о сумме выданных кредитов')
        plt.grid(True)

        months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        plt.xticks(range(1, len(months) + 1), months)

        # Создание легенды
        plt.legend(handles=[
            plt.Rectangle((0, 0), 1, 1, color='SlateBlue'),
            plt.Rectangle((0, 0), 1, 1, color='red')],
            labels=['Больше среднего', 'Меньше среднего'], loc='upper right')

        # Форматирование оси Y в целые числа
        plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))


        # plt.figure(figsize=(10, 6))
        # plt.bar(grouped_data.index, grouped_data.values / 1_000_000, color='SlateBlue')
        # plt.xlabel(f'Месяцы {labels} года')
        # plt.ylabel('Сумма оформленных кредитов (млн.р.)')
        # plt.title('Годовой отчет о сумме выданных кредитов')
        # plt.grid(True)
        # plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))

    # Сохраняем график в файл
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as image_file:
        plt.savefig(image_file.name, bbox_inches='tight')
        plt.close()
        return image_file.name

def get_pandas_dataset_clients():
    model_objects = Clients.objects.all().values()
    dataframe = pd.DataFrame(model_objects)

    return dataframe

def get_pandas_dataset_payroll():
    model_objects = Payroll.objects.all().values()
    dataframe = pd.DataFrame(model_objects)

    return dataframe

def get_pandas_dataset_statement():
    model_objects = CreditStatement.objects.all().values()
    dataframe = pd.DataFrame(model_objects)

    return dataframe

def get_pandas_dataset_types():
    model_objects = LoanTypes.objects.all().values()
    dataframe = pd.DataFrame(model_objects)

    return dataframe

def create_credit_structure(statement, clients, payroll, types):
    merged_df = pd.merge(statement, clients, left_on='client', right_on='id', how='left')
    merged_df = merged_df.dropna()
    merged_df = pd.merge(merged_df, types, left_on='loan_type', right_on='id', how='left')
    merged_df = merged_df.dropna()
    merged_df = pd.merge(payroll, merged_df, left_on='loan', right_on='id_x', how='left')
    merged_df = merged_df.dropna()

    return merged_df


# Помощь и о приложении

def about_page(request):
    return render(request, 'bank/about_page.html')

def help_page(request):
    return render(request, 'bank/help_page.html')

# Заявки

def application_page(request):
    return render(request, 'bank/left_menu/applications/application_page.html')

def check_income_and_credit_value(month_income, credit_amount, term_month):
    if (month_income*0.5)*term_month >= credit_amount:
        return True
    else:
        return False


def load_or_create_model():
    """ Загружает модель из файла или создаёт новую и сохраняет её. """
    try:
        # Пробуем загрузить существующую модель
        final_model = joblib.load(MODEL_FILEPATH)
    except FileNotFoundError:
        print("Не нашел твой файл :(")
        # Генерируем модель
        final_model = train_and_save_model()
        # Сохраняем модель на диск
        joblib.dump(final_model, MODEL_FILEPATH)
        print("Модель успешно сохранена!")
    return final_model


def train_and_save_model():
    """ Тренировка и возврат готовой модели (этот код помещается внутрь функции predict_client()) """
    DATA_PATH = os.path.join(settings.BASE_DIR, 'bank', 'static', 'bank', 'datasets', 'application_record.csv')
    RECORD_PATH = os.path.join(settings.BASE_DIR, 'bank', 'static', 'bank', 'datasets', 'credit_record.csv')
    # Читаем данные
    data = pd.read_csv(DATA_PATH)
    record = pd.read_csv(RECORD_PATH)

    begin_month = pd.DataFrame(record.groupby(["ID"])["MONTHS_BALANCE"].agg(min))
    begin_month = begin_month.rename(columns={'MONTHS_BALANCE': 'begin_month'})
    new_data = pd.merge(data, begin_month, how="left", on="ID")

    record['dep_value'] = 'No'
    cpunt = record.groupby('ID')['STATUS'].size().reset_index(name='status_count')
    cpunt['dep_value'] = cpunt['status_count'].apply(lambda x: 'Yes' if x > 10 else 'No')
    result = cpunt[['ID', 'dep_value']]

    new_data = pd.merge(new_data, cpunt, how='inner', on='ID')
    new_data['target'] = new_data['dep_value']
    new_data.loc[new_data['target'] == 'Yes', 'target'] = 1
    new_data.loc[new_data['target'] == 'No', 'target'] = 0
    cpunt['dep_value'].value_counts(normalize=True)

    new_data.rename(
        columns={'CODE_GENDER': 'sex', 'FLAG_OWN_CAR': 'flag_own_car', 'FLAG_OWN_REALTY': 'flag_own_property',
                 'CNT_CHILDREN': 'count_children', 'AMT_INCOME_TOTAL': 'month_income',
                 'NAME_EDUCATION_TYPE': 'education_type'}, inplace=True)
    new_data.dropna()
    new_data = new_data.mask(new_data == 'NULL').dropna()

    new_data['sex'] = new_data['sex'].replace(['F', 'M'], [0, 1])
    new_data['flag_own_car'] = new_data['flag_own_car'].replace(['N', 'Y'], [0, 1])
    new_data['flag_own_property'] = new_data['flag_own_property'].replace(['N', 'Y'], [0, 1])
    new_data['month_income'] = new_data['month_income'].astype(int)
    new_data['education_type'] = new_data['education_type'].replace(
        ['Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary',
         'Academic degree'], [0, 1, 0, 1, 1])

    new_data = new_data[['sex', 'flag_own_car', 'flag_own_property',
                         'count_children', 'month_income', 'target',
                         'education_type']]
    Y = new_data['target'].astype(int)

    for col in new_data.select_dtypes(include=[bool]):
        new_data[col] = new_data[col].astype(int)
    new_data = new_data.select_dtypes(exclude=[object])

    X = new_data

    np.random.seed(51)
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.3,
                                                        random_state=51,
                                                        stratify=Y)

    normalizer = preprocessing.StandardScaler()
    X_real_norm_np = normalizer.fit_transform(X_train)
    X_train = pd.DataFrame(data=X_real_norm_np, columns=X_test.columns)

    X_real_norm_np = normalizer.transform(X_test)
    X_test = pd.DataFrame(data=X_real_norm_np, columns=X_train.columns)

    param_grid = {
        'C': [0.1, 1, 10],  # Значения коэффициента регуляризации
        'gamma': ['scale', 'auto', 0.1]  # Гамма с автоматическим выбором и вручную заданными значениями
    }

    # Инициализируем модель SVM с RBF-ядром
    svc_rbf = SVC(kernel='rbf', class_weight='balanced')
    # Используем GridSearchCV для нахождения лучших параметров
    grid_search = GridSearchCV(svc_rbf, param_grid, cv=3, n_jobs=-1, verbose=1, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    final_model = SVC(**best_params, kernel='rbf', class_weight='balanced')
    final_model.fit(X_train, y_train)

    return final_model


def predict_client(y):
    global final_model
    # Загружаем модель из файла или создаём новую
    final_model = load_or_create_model()
    prediction = final_model.predict(y)
    return prediction

# Функция для формирования DataFrame из объекта клиента
def create_dataframe(client):
    data = {
        'sex': [client.sex],
        'flag_own_car': [client.flag_own_car],
        'flag_own_property': [client.flag_own_property],
        'count_children': [client.count_children],
        'month_income': [client.month_income],
        'education_type': [client.education_type],
    }

    df = pd.DataFrame(data)
    df['sex'] = df['sex'].replace(['Женский', 'Мужской'], [0, 1])
    df['education_type'] = df['education_type'].replace(['Среднее специальное', 'Высшее'], [0, 1])
    return df

def analysis(request):
    if request.method == 'POST':
        # Получаем данные
        errors = {}
        number_of_the_loan_agreement = request.POST.get('my_field_number_of_the_loan_agreement')
        if not isinstance(number_of_the_loan_agreement, str):
            errors['number'] = 'Номер кредитного договора обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not number_of_the_loan_agreement.isdigit() or int(number_of_the_loan_agreement) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['number'] = 'Номер кредитного договора должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        credit_amount = request.POST.get('my_field_credit_amount')
        if not isinstance(credit_amount, str):
            errors['amount'] = 'Сумма кредита обязательная для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not credit_amount.isdigit() or int(credit_amount) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['amount'] = 'Сумма кредита должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        term_month = request.POST.get('my_term_month')
        if not isinstance(term_month, str):
            errors['month'] = 'Длительность выплат обязательна для заполнения'
            return JsonResponse({'success': False, 'errors': errors})
        elif not term_month.isdigit() or int(term_month) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['month'] = 'Длительность выплат должна быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        loan_type = request.POST.get('my_field_loan_type')
        if not isinstance(loan_type, str):
            errors['loanType'] = 'Регистр. номер типа кредита обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not loan_type.isdigit() or int(loan_type) <= 0:
            # Если введено не число, сообщаем об ошибке
            errors['loanType'] = 'Регистр. номер типа кредита должен быть числовым положительным значением'
            return JsonResponse({'success': False, 'errors': errors})

        client_passport = request.POST.get('my_field_client')
        if not isinstance(client_passport, str):
            errors['client'] = 'Паспорт клиента обязателен для заполнения.'
            return JsonResponse({'success': False, 'errors': errors})
        elif not client_passport.isdigit() or int(client_passport) <= 0 or not re.match(r'\d{10}', client_passport):
            errors['client'] = 'Серия и номер паспорта должны быть числовым положительным значением, состоящим из 10 цифр'
            return JsonResponse({'success': False, 'errors': errors})

        if 'number' not in errors:
            if CreditStatement.objects.filter(number_of_the_loan_agreement=int(number_of_the_loan_agreement)).exists():
                errors['number'] = "Кредит с таким номером договора уже существует"
                return JsonResponse({'success': False, 'errors': errors})

        if 'loanType' not in errors:
            try:
                # Попытка получения объекта LoanType
                loan_t = LoanTypes.objects.get(registration_number=int(loan_type))
            except LoanTypes.DoesNotExist:
                errors['loanType'] = f'Тип кредита с регистрационным номером {loan_type} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if 'client' not in errors:
            try:
                # Попытка получения объекта Client
                client = Clients.objects.get(passport_serial_number=int(client_passport))
            except Clients.DoesNotExist:
                errors['client'] = f'Клиент с паспортными данными {client_passport} не найден.'
                return JsonResponse({'success': False, 'errors': errors})

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        percent = loan_t.interest_rate
        monthly_payment = math.ceil((int(credit_amount) * (percent / 100 + 1.0)) / int(term_month))
        # составление пандас элемента
        y = create_dataframe(client);
        # предсказание ML подели
        prediction = predict_client(y)
        # если предсказано 0, то проверка соответствия выплаты, длительности выплат и ЗП
        if ((int(client.month_income)*0.3 >= int(monthly_payment)) or (prediction == 0)) and check_income_and_credit_value(int(client.month_income), int(credit_amount), int(term_month)):
            try:
                today = date.today()
                formatted_date = today.strftime('%Y-%m-%d')
                statement = CreditStatement(
                    number_of_the_loan_agreement = number_of_the_loan_agreement,
                    credit_amount = credit_amount,
                    term_month = term_month,
                    monthly_payment = monthly_payment,
                    loan_opening_date = formatted_date,
                    repayment_status = 0,
                    loan_type = loan_t,
                    client = client
                )
                statement.save()
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

            try:
                pay = Payroll(
                    loan=CreditStatement.objects.get(number_of_the_loan_agreement=number_of_the_loan_agreement),
                    payment_date=formatted_date,
                    payment_status='C'
                )
                pay.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        else:
            return JsonResponse({'success': False, 'error': 'Отправленная на анализ кредитная заявка не одобрена системой. Все равно хотите сохранить заявку в системе?'})
