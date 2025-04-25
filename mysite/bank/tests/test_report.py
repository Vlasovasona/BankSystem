from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from unittest.mock import patch, MagicMock
from ..views import create_report
from ..models import Clients, LoanTypes, CreditStatement
from django.urls import reverse
from django.test.client import Client
import json
import os

class TestCreateReport(TestCase):
    def setUp(self):
        # Создаем клиентский объект
        self.client = Client()

        # Тестовые объекты вручную
        self.client1 = Clients.objects.create(
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
            registration_number=32,
            name_of_the_type='Ипотечный',
            interest_rate=20.5
        )

        # Создаем объект кредитной ведомости (CreditStatement)
        self.statement = CreditStatement.objects.create(
            number_of_the_loan_agreement=12,
            credit_amount=1000,
            term_month=12,
            monthly_payment=200,
            loan_opening_date='2025-12-09',
            repayment_status=0,
            loan_type=self.type1,
            client=self.client1
        )

        # URL для тестирования
        self.url = reverse('bank:create_report')

    def test_get_request_returns_error(self):
        """GET-запрос не поддерживается"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'error': 'Метод не поддерживается'})

    def test_post_request_with_correct_data(self):
        """Тест успешной генерации отчёта с корректными данными"""
        data = {
            'tables': [
                'Clients',
                'LoanTypes',
                'CreditStatement'
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')
        self.assertRegex(response.get('Content-Disposition'), r'^attachment; filename="output\.pdf"$')

    def test_pdf_creation(self):
        """Проверка факта создания PDF-файла"""
        data = {
            'tables': [
                'Clients',
                'LoanTypes',
                'CreditStatement'
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')

    def test_multiple_tables(self):
        """Тестируем генерацию отчёта с несколькими выбранными таблицами"""
        data = {
            'tables': [
                'Clients',
                'LoanTypes',
                'CreditStatement'
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')

    def test_chart_generation(self):
        """Тестируем генерацию графиков в отчёте"""
        data = {
            'tables': [
                'CreditStructure',
                'Year'
            ]
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')