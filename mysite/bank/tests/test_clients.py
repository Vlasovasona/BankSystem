import random
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
# from mysite.bank.models import Clients
# from mysite.bank.views import ClientListView, client_detail, get_object_or_404, check_clients_fields, search_clients
from ..models import Clients  # Относительный импорт
from ..views import ClientListView, client_detail, check_clients_fields, search_clients

class TestClients(TestCase):

    def setUp(self):
        self.client = Client()
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
        self.client2 = Clients.objects.create(
            surname='Петров',
            name='Пётр',
            patronymic='Петрович',
            phone_number=89001234568,
            age=35,
            sex='Мужской',
            flag_own_car=1,
            flag_own_property=0,
            month_income=60000,
            count_children=1,
            education_type='Среднее',
            passport_serial_number=9876543210
        )

    def test_client_list_view(self):
        """Тестируем представление списка клиентов."""
        response = self.client.get(reverse('bank:clients_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/clients/list.html')  # Проверяем шаблон
        self.assertTrue(len(response.context['clients']) <= 25)  # Проверяем пагинацию

    def test_client_detail_view_valid_id(self):
        """Тестируем представление деталей клиента с валидным идентификатором."""
        valid_client = Clients.objects.first()  # Берем первого клиента из базы
        url = reverse('bank:client_detail', args=(valid_client.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/clients/detail.html')  # Проверяем шаблон
        self.assertEqual(response.context['client'], valid_client)  # Проверяем объект клиента

    def test_client_detail_view_invalid_id(self):
        """Тестируем представление с несуществующим клиентом."""
        invalid_id = Clients.objects.last().id + 1  # Несуществующий идентификатор
        url = reverse('bank:client_detail', args=(invalid_id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_check_clients_fields(self):
        """Тестирование представления с существующим клиентом"""
        errors = {}
        fields = ['passport', 'surname', 'name', 'patronymic', 'phone',
                  'age', 'sex', 'car', 'property', 'income', 'children',
                  'education']
        check_clients_fields('',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             '',
                             errors)
        self.assertCountEqual(list(errors.keys()), fields)

    def test_check_clients_none_fields(self):
        """Тестирование проверки корректности введенных полей кликнта"""
        errors = {}
        fields = ['passport', 'surname', 'name', 'patronymic', 'phone',
                  'age', 'sex', 'car', 'property', 'income', 'children',
                  'education']
        check_clients_fields('',
                             '',
                             '',
                             '',
                             '',
                             None,
                             None,
                             None,
                             None,
                             None,
                             None,
                             None,
                             errors)
        self.assertCountEqual(list(errors.keys()), fields)

    def test_check_clients_incorrect_age(self):
        """Тестирование проверки корректности введенных полей кликнта"""
        errors = {}
        fields = ['passport', 'surname', 'name', 'patronymic', 'phone',
                  'age', 'sex', 'car', 'property', 'income', 'children',
                  'education']
        check_clients_fields('',
                             '',
                             '',
                             '',
                             '',
                             '123',
                             None,
                             None,
                             None,
                             None,
                             None,
                             None,
                             errors)
        self.assertCountEqual(list(errors.keys()), fields)

    def test_search_clients_with_valid_passport(self):
        """Тестирование поиска по номеру паспорта."""
        data = {'search_query': str(self.client1.passport_serial_number)}
        response = self.client.post(reverse('bank:search_clients'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.client1, response.context['clients'])

    def test_search_clients_with_invalid_passport(self):
        """Тестирование поиска по несуществующему номеру паспорта."""
        data = {'search_query': '000'}
        response = self.client.post(reverse('bank:search_clients'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['clients']), 0)

    def test_search_clients_get_request(self):
        """Тестирование интерфейса при GET-запросе."""
        response = self.client.get(reverse('bank:search_clients'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/clients/list.html')
