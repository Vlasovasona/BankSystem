import datetime
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import CreditStatement, Clients, LoanTypes, Payroll
from ..views import (PayrollListView, payroll_detail, check_credit_and_payment_exists,
                     update_repayment_status_after_input_new_pay, validate_loan_id,
                     validate_date)

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
        self.payroll = Payroll.objects.create(
            id=1,
            loan = self.statement,
            payment_date=datetime.date(2026, 1, 9),
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
            self.assertEqual(stmt.payment_date, datetime.date(2026, 1, 9))
            self.assertEqual(stmt.payment_status, '0')

    def test_validate_loan_id(self):
        errors = {}
        validate_loan_id(None, errors)
        self.assertIn('loan', errors)

    def test_validate_date(self):
        errors = {}
        validate_date('2020-08-08', errors)
        self.assertEqual({}, errors)