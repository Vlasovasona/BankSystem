import datetime
import json
from urllib.parse import urlencode
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import CreditStatement, Clients, LoanTypes, Payroll
from ..views import (PayrollListView, payroll_detail, check_credit_and_payment_exists,
                     update_repayment_status_after_input_new_pay, validate_loan_id,
                     validate_date, calculate_payment_status)

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
            term_month=1,
            monthly_payment=200,
            loan_opening_date=datetime.date(2025, 12, 9),
            repayment_status=False,
            client=self.client1,
            loan_type=self.type1
        )
        self.payroll = Payroll.objects.create(
            id=1,
            loan = self.statement,
            payment_date=datetime.date(2025, 1, 9),
            payment_status=0
        )

    def test_payroll_list_view(self):
        """Тестируем представление списка платежей."""
        response = self.client.get(reverse('bank:payroll_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/payroll/list.html')
        self.assertTrue(len(response.context['payroll']) <= 25)

    def test_payroll_detail_view_valid_id(self):
        """Тестируем представление деталей платежа с валидным идентификатором."""
        valid_type = Payroll.objects.first()
        url = reverse('bank:payroll_detail', args=(valid_type.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/payroll/detail.html')
        self.assertEqual(response.context['pay'], valid_type)

    def test_payroll_detail_view_invalid_id(self):
        """Тестируем представление с несуществующим платежом."""
        invalid_id = Payroll.objects.last().id + 1
        url = reverse('bank:payroll_detail', args=(invalid_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_check_payroll_fields(self):
        """Проверка полей платежа."""
        pays = Payroll.objects.all()
        for stmt in pays:
            self.assertEqual(stmt.id, 1)
            self.assertEqual(stmt.loan.number_of_the_loan_agreement, 12)
            self.assertEqual(stmt.payment_date, datetime.date(2025, 1, 9))
            self.assertEqual(stmt.payment_status, '0')

    def test_validate_loan_id_none_data(self):
        errors = {}
        validate_loan_id(None, errors)
        self.assertIn('loan', errors)

    def test_validate_loan_id_incorrect_data(self):
        errors = {}
        validate_loan_id('None', errors)
        self.assertIn('loan', errors)

    def test_validate_date_correct_data(self):
        errors = {}
        validate_date('2020-08-08', errors)
        self.assertEqual({}, errors)

    def test_validate_date_incorrect_format(self):
        errors = {}
        validate_date('nj', errors)
        self.assertIn('date', errors)

    def test_validate_date_incorrect_year(self):
        errors = {}
        validate_date('1000-09-09', errors)
        self.assertIn('date', errors)

    def test_validate_date_incorrect_month(self):
        errors = {}
        validate_date('2020-99-09', errors)
        self.assertIn('date', errors)

    def test_validate_date_incorrect_date(self):
        errors = {}
        validate_date('2020-09-99', errors)
        self.assertIn('date', errors)

    def test_calculate_payment_status_correct_data(self):
        new_data = datetime.date(2025, 4, 24)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('C', payment_status)

    def test_calculate_payment_status_error_data_is_exist(self):
        new_data = datetime.date(2025, 4, 24)
        last_data = datetime.date(2025, 4, 24)
        create_data = datetime.date(2025, 3, 24)

        with self.assertRaises(ValueError) as context:
            calculate_payment_status(
                new_data=new_data,
                last_data=last_data,
                create_data=create_data
            )

        self.assertEqual(str(context.exception), 'По этому кредиту уже была выплата в этом месяце.')

    def test_calculate_payment_status_zero(self):
        new_data = datetime.date(2025, 4, 29)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('0', payment_status)

    def test_calculate_payment_status_one(self):
        new_data = datetime.date(2025, 5, 29)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('1', payment_status)

    def test_calculate_payment_status_two(self):
        new_data = datetime.date(2025, 6, 29)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('2', payment_status)

    def test_calculate_payment_status_three(self):
        new_data = datetime.date(2025, 7, 29)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('3', payment_status)

    def test_calculate_payment_status_four(self):
        new_data = datetime.date(2025, 8, 29)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('4', payment_status)

    def test_calculate_payment_status_five(self):
        new_data = datetime.date(2026, 8, 9)
        last_data = datetime.date(2025, 3, 24)
        create_data = datetime.date(2025, 2, 24)

        payment_status = calculate_payment_status(new_data=new_data,
                                                  last_data=last_data,
                                                  create_data=create_data)

        self.assertEqual('5', payment_status)

    def test_payroll_add_detail_view(self):
        """Тестируем представление окна добавления нового платежа."""
        response = self.client.get(reverse('bank:payroll_add_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/payroll/add_detail.html')

    def test_valid_deletion(self):
        """ Корректный запрос на удаление существующего платежа. """
        response = self.client.post(reverse('bank:delete_single_payroll'),
                                    data=json.dumps({"pay_id": self.payroll.id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertFalse(
            Payroll.objects.filter(id=self.payroll.id).exists())  # Проверяем, что запись действительно удалена

    def test_nonexistent_loan_type(self):
        """ Попытка удалить несуществующего платежа. """
        non_existent_id = 999999  # ID, которого точно нет в БД
        response = self.client.post(reverse('bank:delete_single_payroll'),
                                    data=json.dumps({"pay_id": non_existent_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['error'], f"Платежа с ID {non_existent_id} не существует.")

    def test_invalid_loan_type_id_format(self):
        """ Неверный формат идентификатора (нечисловое значение). """
        bad_id = "abc"
        response = self.client.post(reverse('bank:delete_single_payroll'),
                                    data=json.dumps({"pay_id": bad_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], f"Передано неверное значение ID: {bad_id}.")

    def test_missing_loan_type_id_field(self):
        """ Отсутствие параметра 'loan_id'. """
        response = self.client.post(reverse('bank:delete_single_payroll'),
                                    data={},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'pay_id'.")

    def test_bad_json_structure(self):
        """ Некорректная структура JSON. """
        malformed_json = {"invalid_key": "value"}
        response = self.client.post(reverse('bank:delete_single_payroll'),
                                    data=json.dumps(malformed_json),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'pay_id'.")

    def test_wrong_http_method(self):
        """ Использование неправильного HTTP-метода (GET вместо POST). """
        response = self.client.get(reverse('bank:delete_single_payroll'))

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(json.loads(response.content), {})

    def test_update_repayment_status_after_input_new_pay(self):
        update_repayment_status_after_input_new_pay(self.statement)
        self.assertEqual(self.statement.repayment_status, 1)

    def test_check_credit_and_payment_exists(self):
        success, errors = check_credit_and_payment_exists(self.statement.number_of_the_loan_agreement,
                                        self.payroll.payment_date)

        self.assertEqual(success, False)
        self.assertIn('date', errors)
        self.assertEqual(errors['date'], "Для этого кредита в эту дату уже был внесен платеж!")

    def test_check_credit_and_payment_exists_incorrect_number_of_the_agreement(self):
        success, errors = check_credit_and_payment_exists(self.statement.id,
                                        self.payroll.payment_date)

        self.assertEqual(success, False)
        self.assertIn('loan', errors)
        self.assertEqual(errors['loan'], 'Запись с таким номером договора не найдена')

    def test_update_pay_successful(self):
        """Корректное обновление данных платежа"""
        new_data = {
            'pay_id': self.payroll.pk,
            'my_field_loan': str(self.statement.number_of_the_loan_agreement),
            'my_field_payment_date': '2025-05-09'
        }

        # Отправляем данные с correct Content-Type
        response = self.client.post(reverse('bank:update-payroll'), new_data)

        updated_pay = Payroll.objects.get(pk=self.payroll.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(updated_pay.loan.number_of_the_loan_agreement, int(new_data['my_field_loan']))
        self.assertEqual(updated_pay.payment_status, '3')
        self.assertEqual(updated_pay.payment_date, datetime.date(2025, 5, 9))

    def test_update_pay_with_errors(self):
        """Обновление платежа с некорректными данными"""
        incorrect_data = {
            'pay_id': self.payroll.pk,
            'my_field_loan': '',
            'my_field_payment_date': '1000-05-09'
        }

        response = self.client.post(reverse('bank:update-payroll'), incorrect_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(errors)
        self.assertIn('loan', errors.keys())
        self.assertIn('date', errors.keys())

    # def test_update_pay_not_found(self):
    #     """Попробуем обновить несуществующий платеж"""
    #     data = {
    #         'pay_id': self.payroll.pk,
    #         'my_field_loan': '9999',
    #         'my_field_payment_date': '2024-05-09'
    #     }
    #
    #     response = self.client.post(reverse('bank:update-payroll'), data)
    #     response_content = json.loads(response.content)
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(response_content['success'])
    #     self.assertEqual(response_content['error'], 'Запись с таким номером договора не найдена')


    def test_update_pay_with_duplicate_fields(self):
        """Обновление платежа с дублирующимся"""
        duplicate_data = {
            'pay_id': self.payroll.id,
            'my_field_loan': str(self.statement.number_of_the_loan_agreement),
            'my_field_payment_date': '2025-01-09'
        }

        response = self.client.post(reverse('bank:update-payroll'), duplicate_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('date', errors.keys())
        self.assertEqual(errors['date'],  "Для этого кредита в эту дату уже был внесен платеж!")

    # def test_update_pay_without_required_field(self):
    #     """Обновление платежа без обязательного поля"""
    #     incomplete_data = {
    #         'pay_id': self.payroll.id,
    #         'my_field_loan': str(self.statement.number_of_the_loan_agreement),
    #         'my_field_payment_date': '2026-01-09'
    #     }
    #
    #     response = self.client.post(reverse('bank:update-payroll'), incomplete_data)
    #     errors = json.loads(response.content)['errors']
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('surname', errors.keys())








