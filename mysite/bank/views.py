# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, LoanTypes, Payroll
from django.views.generic import ListView
from django.db.models import Q
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm


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

def update_loan_type(request):
    """Осуществление изменение типа кредита в БД."""
    if request.method == 'POST':
        # Получаем данные
        credit_type_id = request.POST.get('credit_type_id')
        registration_number = request.POST.get('my_field_credit_type_code')
        name_of_the_type = request.POST.get('my_field_credit_type_name')
        interest_rate = request.POST.get('my_field_credit_percent')

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
        loan_id = request.POST.get('my_field_loan')
        payment_date = request.POST.get('my_field_payment_date')
        payment_status = request.POST.get('my_field_payment_status')

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
        # Получаем данные
        statement_id = request.POST.get('credit_state_id')
        number_of_the_loan_agreement = request.POST.get('my_field_number_of_the_loan_agreement')
        credit_amount = request.POST.get('my_field_credit_amount')
        term_month = request.POST.get('my_term_month')
        monthly_payment = request.POST.get('my_field_monthly_payment')
        loan_opening_date = request.POST.get('my_field_loan_opening_date')
        repayment_status = request.POST.get('my_field_repayment_status')
        loan_type = request.POST.get('my_field_loan_type')
        client_passport = request.POST.get('my_field_client')

        try:
            # Попытка получения объекта LoanType
            loan_t = LoanTypes.objects.get(registration_number=loan_type)
        except LoanTypes.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Тип кредита с регистрационным номером {loan_type} не найден.'
            })

        try:
            # Попытка получения объекта Client
            client = Clients.objects.get(passport_serial_number=client_passport)
        except Clients.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Клиент с паспортными данными {client_passport} не найден.'
            })

        try:
            statement = CreditStatement.objects.get(pk=statement_id)
            # Обновляем поля
            statement.number_of_the_loan_agreement = number_of_the_loan_agreement
            statement.credit_amount = credit_amount
            statement.term_month = term_month
            statement.monthly_payment = monthly_payment
            statement.loan_opening_date = loan_opening_date
            statement.repayment_status = 1 if repayment_status.strip() == 'Да' else 0
            statement.loan_type = loan_t
            statement.client = client
            statement.save()
            return JsonResponse({'success': True})

        except Payroll.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Кредитный договор {statement_id} не найден.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_client(request):
    """Осуществление добавления клиента в БД."""
    if request.method == 'POST':
        # Получаем данные
        passport = request.POST.get('my_field_passport')
        surname = request.POST.get('my_field_surname')
        name = request.POST.get('my_field_name')
        patronymic = request.POST.get('my_field_patronymic')
        adress = request.POST.get('my_field_adress')
        phone_number = request.POST.get('my_field_phone')
        age = request.POST.get('my_field_age')
        sex = request.POST.get('my_field_sex')
        flag_own_car = request.POST.get('my_field_flag_own_car')
        flag_own_property = request.POST.get('my_flag_own_property')
        month_income = request.POST.get('my_field_month_income')
        count_children = request.POST.get('my_field_count_children')
        education_type = request.POST.get('my_field_education_type')

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

def add_new_loan_type(request):
    """Осуществление добавления типа кредита в БД."""
    if request.method == 'POST':
        # Получаем данные
        registration_number = request.POST.get('my_field_credit_type_code')
        name_of_the_type = request.POST.get('my_field_credit_type_name')
        interest_rate = request.POST.get('my_field_credit_percent')

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
        loan_id = request.POST.get('my_field_loan')
        payment_date = request.POST.get('my_field_payment_date')
        payment_status = request.POST.get('my_field_payment_status')

        try:
            # Попытка получения объекта CreditStatement
            loan = CreditStatement.objects.get(number_of_the_loan_agreement=loan_id)
        except CreditStatement.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Запись в ведомости с номером договора {loan_id} не найдена.'
            })

        try:
            pay = Payroll(
                loan = loan,
                payment_date = payment_date,
                payment_status = payment_status
            )
            pay.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def add_new_credit_statement(request):
    """Осуществление добавления кредитного договора в БД."""
    if request.method == 'POST':
        # Получаем данные
        number_of_the_loan_agreement = request.POST.get('my_field_number_of_the_loan_agreement')
        credit_amount = request.POST.get('my_field_credit_amount')
        term_month = request.POST.get('my_term_month')
        monthly_payment = request.POST.get('my_field_monthly_payment')
        loan_opening_date = request.POST.get('my_field_loan_opening_date')
        repayment_status = request.POST.get('my_field_repayment_status')
        loan_type = request.POST.get('my_field_loan_type')
        client_passport = request.POST.get('my_field_client')

        try:
            # Попытка получения объекта LoanType
            loan_t = LoanTypes.objects.get(registration_number=loan_type)
        except LoanTypes.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Тип кредита с регистрационным номером {loan_type} не найден.'
            })

        try:
            # Попытка получения объекта Client
            client = Clients.objects.get(passport_serial_number=client_passport)
        except Clients.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Клиент с паспортными данными {client_passport} не найден.'
            })

        try:
            statement = CreditStatement(
                number_of_the_loan_agreement = number_of_the_loan_agreement,
                credit_amount = credit_amount,
                term_month = term_month,
                monthly_payment = monthly_payment,
                loan_opening_date = loan_opening_date,
                repayment_status = 1 if repayment_status.strip() == 'Да' else 0,
                loan_type = loan_t,
                client = client
            )
            statement.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


# def register_view(request):
#     if request.method == 'POST': # если запрос POST, то пользователь передает данные для регистрации, создаем новую учетную запись
#         form = UserCreationForm(request.POST) # встроенная форма Django для регистрации пользователя
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/bank/clients/') # Переадресация после успешной регистрации
#     else: # если метод GET - значит, нужно отобразить пустую страницу для заполнения пользователем регистрационных полей
#         form = UserCreationForm()
#
#     context = {'form': form} # передаем форму в html-шаблон для отображения
#     return render(request, 'bank/registrationPage.html', context)

def register_view(request):
    """Осуществление регистрации нового юзера."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняет нового пользователя с указанным email и статусом staff
            login(request, user)
            return redirect('/bank/clients/')
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