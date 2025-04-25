import datetime
import json
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import CreditStatement, Clients, LoanTypes
from ..views import CreditTypesListView, credit_statement_detail, check_credit_statement

class TestCreditTypes(TestCase):
    def setUp(self):
        # Создаем клиентский объект
        self.client = Client()

        self.client1 = Clients.objects.create(
            id=1,
            surname='Иванов',
            name='Иван',
            patronymic='Иванович',
            phone_number=89001234567,
            age=30,
            sex='Мужской',
            flag_own_car=0,
            flag_own_property=1,
            month_income=50000,
            count_children=2,
            education_type='Высшее',
            passport_serial_number=1234567890
        )
        self.type1 = LoanTypes.objects.create(
            id=1,
            registration_number=32,
            name_of_the_type='Ипотечный',
            interest_rate=20.5
        )
        # Создаем объект кредитной ведомости (CreditStatement)
        self.statement = CreditStatement.objects.create(
            id=1,
            number_of_the_loan_agreement=12,
            credit_amount=1000,
            term_month=12,
            monthly_payment=200,
            loan_opening_date=datetime.date(2025, 12, 9),
            repayment_status=False,
            client=self.client1,
            loan_type=self.type1
        )

    def test_credit_statement_list_view(self):
        """Тестируем представление списка кредитной ведомости."""
        response = self.client.get(reverse('bank:credit_statement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditStatement/list.html')
        self.assertTrue(len(response.context['credit_statement']) <= 25)

    def test_credit_statement_detail_view_valid_id(self):
        """Тестируем представление деталей ведомости с валидным идентификатором."""
        valid_type = CreditStatement.objects.first()
        url = reverse('bank:credit_statement_detail', args=(valid_type.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditStatement/detail.html')
        self.assertEqual(response.context['credit_statement_item'], valid_type)

    def test_credit_statement_detail_view_invalid_id(self):
        """Тестируем представление с несуществующей ведомостью."""
        invalid_id = CreditStatement.objects.last().id + 1
        url = reverse('bank:credit_statement_detail', args=(invalid_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_check_credit_statement_fields(self):
        """Проверка полей кредитной ведомости."""
        created_statements = CreditStatement.objects.all()
        for stmt in created_statements:
            self.assertEqual(stmt.number_of_the_loan_agreement, 12)
            self.assertEqual(stmt.credit_amount, 1000)
            self.assertEqual(stmt.term_month, 12)
            self.assertEqual(stmt.monthly_payment, 200)
            self.assertEqual(stmt.loan_type.registration_number, 32)
            self.assertEqual(stmt.client.surname, 'Иванов')

    def test_check_credit_statement_none_values(self):
        errors = {}
        check_credit_statement(number_of_the_loan_agreement=None,
                               credit_amount=None,
                               term_month=None,
                               loan_type=None,
                               client_passport=None,
                               errors=errors)
        self.assertIn('number', errors)
        self.assertIn('amount', errors)
        self.assertIn('month', errors)
        self.assertIn('loanType', errors)
        self.assertIn('client', errors)

    def test_check_credit_statement_incorrect_values(self):
        errors = {}
        check_credit_statement(number_of_the_loan_agreement='None',
                               credit_amount='None',
                               term_month='None',
                               loan_type='None',
                               client_passport='',
                               errors=errors)
        self.assertIn('number', errors)
        self.assertIn('amount', errors)
        self.assertIn('month', errors)
        self.assertIn('loanType', errors)
        self.assertIn('client', errors)

    def test_credit_statement_add_detail_view(self):
        """Тестируем представление окна добавления нового кредита."""
        response = self.client.get(reverse('bank:credit_statement_add_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditStatement/add_detail.html')

    def test_valid_deletion(self):
        """ Корректный запрос на удаление существующего кредита. """
        response = self.client.post(reverse('bank:delete_single_statement'),
                                    data=json.dumps({"credit_state_id": self.statement.id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertFalse(
            CreditStatement.objects.filter(id=self.statement.id).exists())  # Проверяем, что запись действительно удалена

    def test_nonexistent_loan_type(self):
        """ Попытка удалить несуществующего кредита. """
        non_existent_id = 999999  # ID, которого точно нет в БД
        response = self.client.post(reverse('bank:delete_single_statement'),
                                    data=json.dumps({"credit_state_id": non_existent_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['error'], f"Договора с ID {non_existent_id} не существует.")

    def test_invalid_loan_type_id_format(self):
        """ Неверный формат идентификатора (нечисловое значение). """
        bad_id = "abc"
        response = self.client.post(reverse('bank:delete_single_statement'),
                                    data=json.dumps({"credit_state_id": bad_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], f"Передано неверное значение ID: {bad_id}.")

    def test_missing_loan_type_id_field(self):
        """ Отсутствие параметра 'loan_id'. """
        response = self.client.post(reverse('bank:delete_single_statement'),
                                    data={},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'credit_state_id'.")

    def test_bad_json_structure(self):
        """ Некорректная структура JSON. """
        malformed_json = {"invalid_key": "value"}
        response = self.client.post(reverse('bank:delete_single_statement'),
                                    data=json.dumps(malformed_json),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'credit_state_id'.")

    def test_wrong_http_method(self):
        """ Использование неправильного HTTP-метода (GET вместо POST). """
        response = self.client.get(reverse('bank:delete_single_statement'))

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(json.loads(response.content), {})

    def test_update_statement_successful(self):
        """Корректное обновление данных ведомости"""
        new_data = {
            'credit_state_id': self.statement.pk,
            'my_field_number_of_the_loan_agreement': str(self.statement.number_of_the_loan_agreement),
            'my_field_credit_amount': '10000',
            'my_term_month': '12',
            'my_field_loan_type': str(self.type1.registration_number),
            'my_field_client': str(self.client1.passport_serial_number),
        }

        # Отправляем данные с correct Content-Type
        response = self.client.post(reverse('bank:update-credit-statement'), new_data)

        updated_statement = CreditStatement.objects.get(pk=self.statement.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(updated_statement.number_of_the_loan_agreement, int(new_data['my_field_number_of_the_loan_agreement']))
        self.assertEqual(updated_statement.credit_amount, int(new_data['my_field_credit_amount']))
        self.assertEqual(updated_statement.term_month, int(new_data['my_term_month']))
        self.assertEqual(updated_statement.repayment_status, False)
        self.assertEqual(updated_statement.loan_type, self.type1)
        self.assertEqual(updated_statement.client, self.client1)


    def test_update_statement_with_errors(self):
        """Обновление кредита с некорректными данными"""
        incorrect_data = {
            'credit_state_id': self.statement.pk,
            'my_field_number_of_the_loan_agreement': str(self.statement.number_of_the_loan_agreement),
            'my_field_credit_amount': '',
            'my_term_month': '',
            'my_field_loan_type': str(self.type1.registration_number),
            'my_field_client': str(self.client1.passport_serial_number),
        }

        response = self.client.post(reverse('bank:update-credit-statement'), incorrect_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(errors)
        self.assertIn('amount', errors.keys())
        self.assertIn('month', errors.keys())

    def test_update_statement_with_not_existing_type(self):
        """Обновление платежа с некорректным типом кредита"""
        incorrect_type = '11000'
        duplicate_data = {
            'credit_state_id': self.statement.pk,
            'my_field_number_of_the_loan_agreement': str(self.statement.number_of_the_loan_agreement),
            'my_field_credit_amount': '123',
            'my_term_month': '123',
            'my_field_loan_type': incorrect_type,
            'my_field_client': str(self.client1.passport_serial_number),
        }

        response = self.client.post(reverse('bank:update-credit-statement'), duplicate_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('loanType', errors.keys())
        self.assertEqual(errors['loanType'],  f'Тип кредита с регистрационным номером {incorrect_type} не найден.')

    def test_add_credit_statement_successfully(self):
        """Проверка успешного добавления кредитного договора"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '100000',
            'my_term_month': '12',
            'my_field_loan_type': '32',
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertIsNotNone(CreditStatement.objects.get(number_of_the_loan_agreement=1000))

    def test_add_existing_credit_statement(self):
        """Проверка невозможности добавить договор с уже существующим номером"""
        # Создаем первый контракт
        first_contract = CreditStatement.objects.create(
            number_of_the_loan_agreement=1000,
            credit_amount=100000,
            term_month=12,
            monthly_payment=10000,
            loan_opening_date=datetime.date.today(),
            repayment_status=0,
            loan_type=self.type1,
            client=self.client1
        )

        # Пробуем создать второй контракт с тем же номером
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '100000',
            'my_term_month': '12',
            'my_field_loan_type': '32',
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('number', response.json()['errors'])
        self.assertEqual(response.json()['errors']['number'], 'Кредит с таким номером договора уже существует')

    def test_add_without_client(self):
        """Проверка попытки добавления контракта без существующего клиента"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '100000',
            'my_term_month': '12',
            'my_field_loan_type': '32',
            'my_field_client': '1234567891'  # Неверный паспорт
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('client', response.json()['errors'])
        self.assertEqual(response.json()['errors']['client'], 'Клиент с паспортными данными 1234567891 не найден.')

    def test_add_without_loan_type(self):
        """Проверка попытки добавления контракта без существующего типа кредита"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '100000',
            'my_term_month': '12',
            'my_field_loan_type': '33',  # Тип кредита с таким регистром не существует
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('loanType', response.json()['errors'])
        self.assertEqual(response.json()['errors']['loanType'], 'Тип кредита с регистрационным номером 33 не найден.')

    def test_add_with_negative_values(self):
        """Проверка добавления контракта с отрицательными значениями суммы кредита или срока"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '-100000',  # Отрицательная сумма кредита
            'my_term_month': '12',
            'my_field_loan_type': '32',
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('amount', response.json()['errors'])
        self.assertEqual(response.json()['errors']['amount'], 'Сумма кредита должна быть числовым положительным значением')

    def test_add_zero_credit_amount(self):
        """Проверка добавления контракта с нулевым значением суммы кредита"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '0',  # Сумма кредита равна нулю
            'my_term_month': '12',
            'my_field_loan_type': '32',
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('amount', response.json()['errors'])
        self.assertEqual(response.json()['errors']['amount'], 'Сумма кредита должна быть числовым положительным значением')

    def test_add_zero_term_month(self):
        """Проверка добавления контракта с нулевым сроком кредита"""
        data = {
            'my_field_number_of_the_loan_agreement': '1000',
            'my_field_credit_amount': '100000',
            'my_term_month': '0',  # Срок кредита равен нулю
            'my_field_loan_type': '32',
            'my_field_client': '1234567890'
        }
        response = self.client.post(reverse('bank:add_new_credit_statement'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('month', response.json()['errors'])
        self.assertEqual(response.json()['errors']['month'],
                         'Длительность выплат должна быть числовым положительным значением')
