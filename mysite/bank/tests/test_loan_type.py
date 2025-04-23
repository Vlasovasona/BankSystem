import random
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import LoanTypes  # Относительный импорт
from ..views import CreditTypesListView, credit_type_detail, check_loan_type

# coverage run manage.py test bank.tests --keepdb -v 2

class TestCreditTypes(TestCase):

    def setUp(self):
        self.client = Client()
        self.type1 = LoanTypes.objects.create(
            registration_number=32,
            name_of_the_type='Ипотечный',
            interest_rate=20.5
        )
        self.type2 = LoanTypes.objects.create(
            registration_number=97,
            name_of_the_type='Льготный',
            interest_rate=9.0
        )

    def test_credit_types_list_view(self):
        """Тестируем представление списка типов кредита."""
        response = self.client.get(reverse('bank:credit_types_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditTypes/list.html')  # Проверяем шаблон
        self.assertTrue(len(response.context['credit_types']) <= 25)  # Проверяем пагинацию

    def test_credit_type_detail_view_valid_id(self):
        """Тестируем представление деталей типа кредита с валидным идентификатором."""
        valid_type = LoanTypes.objects.first()  # Берем первого клиента из базы
        url = reverse('bank:credit_type_detail', args=(valid_type.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditTypes/detail.html')  # Проверяем шаблон
        self.assertEqual(response.context['credit_type'], valid_type)  # Проверяем объект клиента

    def test_client_detail_view_invalid_id(self):
        """Тестируем представление с несуществующим типом."""
        invalid_id = LoanTypes.objects.last().id + 1  # Несуществующий идентификатор
        url = reverse('bank:credit_type_detail', args=(invalid_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_check_clients_fields(self):
        """Тестирование представления с существующим клиентом"""
        errors = {}
        fields = ['credit_types', 'name', 'percent']
        check_loan_type('',
                             12,
                             '',
                             errors,
        )
        self.assertCountEqual(list(errors.keys()), fields)

