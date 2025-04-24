import random
import json
from urllib.parse import urlencode
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from ..models import LoanTypes  # Относительный импорт
from ..views import CreditTypesListView, credit_type_detail, check_loan_type

# coverage run manage.py test bank.tests --keepdb -v 2

class TestCreditTypes(TestCase):

    def setUp(self):
        self.client = Client()
        self.type1 = LoanTypes.objects.create(
            id=1,
            registration_number=32,
            name_of_the_type='Ипотечный',
            interest_rate=20.5
        )
        self.type2 = LoanTypes.objects.create(
            id=2,
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

    def test_check_clients_fields_none_values(self):
        """Тестирование представления с существующим клиентом"""
        errors = {}
        check_loan_type(None,
                             None,
                             None,
                             errors,
        )
        self.assertIn('credit_types', errors)
        self.assertIn('percent', errors)

    def test_loan_type_add_detail_view(self):
        """Тестируем представление окна добавления нового типа кредита."""
        response = self.client.get(reverse('bank:credit_types_add_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/creditTypes/add_detail.html')

    def test_valid_deletion(self):
        """ Корректный запрос на удаление существующего типа кредита. """
        response = self.client.post(reverse('bank:delete_single_loan_type'),
                                    data=json.dumps({"credit_type_id": self.type1.id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertFalse(
            LoanTypes.objects.filter(id=self.type1.id).exists())  # Проверяем, что запись действительно удалена

    def test_nonexistent_loan_type(self):
        """ Попытка удалить несуществующего типа кредита. """
        non_existent_id = 999999  # ID, которого точно нет в БД
        response = self.client.post(reverse('bank:delete_single_loan_type'),
                                    data=json.dumps({"credit_type_id": non_existent_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['error'], f"Договора с ID {non_existent_id} не существует.")

    def test_invalid_loan_type_id_format(self):
        """ Неверный формат идентификатора (нечисловое значение). """
        bad_id = "abc"
        response = self.client.post(reverse('bank:delete_single_loan_type'),
                                    data=json.dumps({"credit_type_id": bad_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], f"Передано неверное значение ID: {bad_id}.")

    def test_missing_loan_type_id_field(self):
        """ Отсутствие параметра 'loan_type_id'. """
        response = self.client.post(reverse('bank:delete_single_loan_type'),
                                    data={},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'loan_type_id'.")

    def test_bad_json_structure(self):
        """ Некорректная структура JSON. """
        malformed_json = {"invalid_key": "value"}
        response = self.client.post(reverse('bank:delete_single_loan_type'),
                                    data=json.dumps(malformed_json),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'loan_type_id'.")

    def test_wrong_http_method(self):
        """ Использование неправильного HTTP-метода (GET вместо POST). """
        response = self.client.get(reverse('bank:delete_single_loan_type'))

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(json.loads(response.content), {})

    def test_update_type_successful(self):
        """Корректное обновление данных типа кредита"""
        new_data = {
            'credit_type_id': self.type1.pk,
            'my_field_credit_type_code': '12345',
            'my_field_credit_type_name': 'Валютный',
            'my_field_credit_percent': '22.0'
        }

        encoded_data = urlencode(new_data)

        response = self.client.post(reverse('bank:update-credit-type'), encoded_data,
                                    content_type='application/x-www-form-urlencoded')

        updated_type = LoanTypes.objects.get(pk=self.type1.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(updated_type.registration_number, int(new_data['my_field_credit_type_code']))
        self.assertEqual(updated_type.name_of_the_type, new_data['my_field_credit_type_name'])
        self.assertEqual(updated_type.interest_rate, float(new_data['my_field_credit_percent']))

    def test_update_type_with_errors(self):
        """Обновление типа кредита с некорректными данными"""
        incorrect_data = {
            'credit_type_id': self.type1.pk,
            'my_field_credit_type_code': 'иппу',
            'my_field_credit_type_name': '',
            'my_field_credit_percent': '22.маы0'
        }

        response = self.client.post(reverse('bank:update-credit-type'), incorrect_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(errors)
        self.assertIn('percent', errors.keys())
        self.assertIn('credit_types', errors.keys())

    def test_update_loan_type_not_found(self):
        """Попробуем обновить несуществующего типа кредита"""
        wrong_id = 999999
        data = {
            'credit_type_id': wrong_id,
            'my_field_credit_type_code': '890',
            'my_field_credit_type_name': '',
            'my_field_credit_percent': '22.0'
        }

        response = self.client.post(reverse('bank:update-credit-type'), data)
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_content['success'])
        self.assertEqual(response_content['error'], f'Тип кредита {wrong_id} не найден.')

    def test_update_type_with_duplicate_number(self):
        """Обновление клиента с дублирующимся номером кредита"""
        duplicate_data = {
            'credit_type_id': self.type1.pk,
            'my_field_credit_type_code': '97',
            'my_field_credit_type_name': '',
            'my_field_credit_percent': '22.0'
        }

        response = self.client.post(reverse('bank:update-credit-type'), duplicate_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('credit_types', errors.keys())
        self.assertEqual(errors['credit_types'], f'Тип кредита с регистрационным номером {int(duplicate_data['my_field_credit_type_code'])} уже существует.')

    def test_update_type_without_required_field(self):
        """Обновление клиента без обязательного поля"""
        incomplete_data = {
            'credit_type_id': self.type1.pk,
            'my_field_credit_type_code': '',
            'my_field_credit_type_name': '',
            'my_field_credit_percent': '22.0'
        }

        response = self.client.post(reverse('bank:update-credit-type'), incomplete_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('credit_types', errors.keys())





