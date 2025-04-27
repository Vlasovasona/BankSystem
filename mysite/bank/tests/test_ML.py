from django.test import TestCase, override_settings, Client
from django.core.exceptions import ValidationError
from ..models import Clients, LoanTypes, CreditStatement
from ..views import analysis
import datetime
from django.urls import reverse

class AnalysisViewTests(TestCase):
    # fixtures = ["test_data.json"]

    def setUp(self):
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
        self.new_data = {
            'my_field_number_of_the_loan_agreement': '1111',
            'my_field_credit_amount': '10000',
            'my_term_month': '12',
            'my_field_loan_type': str(self.type1.registration_number),
            'my_field_client': str(self.client1.passport_serial_number),
        }

    def test_analysis_view_success(self):
        with override_settings(DEBUG=False):
            response = self.client.post(reverse('bank:analysis'), self.new_data)
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': True})

    def test_analysis_view_failure(self):
        # Случаи, когда форма отправляется с ошибочными данными
        invalid_data = {
            'my_field_number_of_the_loan_agreement': '',
            'my_field_credit_amount': '10000',
            'my_term_month': '12',
            'my_field_loan_type': str(self.type1.registration_number),
            'my_field_client': str(self.client1.passport_serial_number),
        }
        response = self.client.post(reverse('bank:analysis'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'success': False,
                              'errors': {'number': 'Номер кредитного договора должен быть числовым положительным значением'}})