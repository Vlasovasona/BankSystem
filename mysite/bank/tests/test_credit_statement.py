import datetime
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import CreditStatement, Clients, LoanTypes
from ..views import CreditTypesListView, credit_statement_detail, check_credit_statement

class TestCreditTypes(TestCase):

    def setUp(self):
        # Создаем клиентский объект
        self.client = Client()

        self.client1 = Clients.objects.get(pk=1)
        self.type1 = LoanTypes.objects.get(pk=1)
        # Создаем объект кредитной ведомости (CreditStatement)
        self.statement = CreditStatement.objects.create(
            number_of_the_loan_agreement=12,
            credit_amount=1000,
            term_month=12,
            monthly_payment=200,
            loan_opening_date=datetime.date(2025, 12, 9),
            repayment_status=False,
            loan_type=self.type1,
            client=self.client1
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
        self.assertEqual(response.context['credit_statement'], valid_type)

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
            self.assertEqual(stmt.loan_type.registration_number, 67)
            self.assertEqual(stmt.client.surname, 'Иванов')