import random
from django.test import TestCase, Client
from django.urls import reverse
import json
from urllib.parse import urlencode
from ..models import Clients  # Относительный импорт
from ..views import check_clients_fields

class TestClients(TestCase):

    def setUp(self):
        self.client = Client()
        self.client1 = Clients.objects.create(
            id=1,
            surname='Иванов',
            name='Иван',
            patronymic='Иванович',
            phone_number=89001234567,
            adress='Москва',
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
            id=2,
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
            education_type='Среднее специальное',
            passport_serial_number=9876543210
        )
        self.client3 = Clients.objects.create(
            id=3,
            surname='Волков',
            name='Евгений',
            patronymic='Викторович',
            phone_number=8900125678,
            age=56,
            sex='Мужской',
            flag_own_car=0,
            flag_own_property=0,
            month_income=6,
            count_children=0,
            education_type='Среднее специальное',
            passport_serial_number=9876599999
        )
        self.url = reverse('bank:update_client_view')

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

    def test_clients_add_detail_view(self):
        """Тестируем представление окна добавления нового типа кредита."""
        response = self.client.get(reverse('bank:client_add_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank/clients/add_detail.html')

    def test_valid_deletion(self):
        """ Корректный запрос на удаление существующего клиента. """
        response = self.client.post(reverse('bank:delete_single_client'),
                                    data=json.dumps({"client_id": self.client1.id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertFalse(
            Clients.objects.filter(id=self.client1.id).exists())  # Проверяем, что запись действительно удалена

    def test_nonexistent_client(self):
        """ Попытка удалить несуществующего клиента. """
        non_existent_id = 999999  # ID, которого точно нет в БД
        response = self.client.post(reverse('bank:delete_single_client'),
                                    data=json.dumps({"client_id": non_existent_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['error'], f"Клиента с ID {non_existent_id} не существует.")

    def test_invalid_client_id_format(self):
        """ Неверный формат идентификатора (нечисловое значение). """
        bad_id = "abc"
        response = self.client.post(reverse('bank:delete_single_client'),
                                    data=json.dumps({"client_id": bad_id}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], f"Передано неверное значение ID: {bad_id}.")

    def test_missing_client_id_field(self):
        """ Отсутствие параметра 'client_id'. """
        response = self.client.post(reverse('bank:delete_single_client'),
                                    data={},
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'client_id'.")

    def test_bad_json_structure(self):
        """ Некорректная структура JSON. """
        malformed_json = {"invalid_key": "value"}
        response = self.client.post(reverse('bank:delete_single_client'),
                                    data=json.dumps(malformed_json),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Не найден параметр 'client_id'.")

    def test_wrong_http_method(self):
        """ Использование неправильного HTTP-метода (GET вместо POST). """
        response = self.client.get(reverse('bank:delete_single_client'))

        self.assertEqual(response.status_code, 405)
        self.assertDictEqual(json.loads(response.content), {})

    def tearDown(self):
         Clients.objects.all().delete()

    def test_update_client_successful(self):
        """Корректное обновление данных клиента"""
        new_data = {
            'client_id': self.client1.pk,
            'my_field_passport': '1234567891',
            'my_field_surname': 'Петрова',
            'my_field_name': 'Анна',
            'my_field_patronymic': 'Павловна',
            'my_field_address': 'парам',
            'my_field_phone': '89997654321',
            'my_field_age': '35',
            'my_field_sex': 'Женский',
            'my_field_flag_own_car': 'Нет',
            'my_flag_own_property': 'Да',
            'my_field_month_income': '60000',
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }

        # Конвертируем данные в формат form/urlencoded
        encoded_data = urlencode(new_data)

        # Отправляем данные с correct Content-Type
        response = self.client.post(reverse('bank:update_client_view'), encoded_data,
                                    content_type='application/x-www-form-urlencoded')

        updated_user = Clients.objects.get(pk=self.client1.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(updated_user.passport_serial_number, int(new_data['my_field_passport']))
        self.assertEqual(updated_user.surname, new_data['my_field_surname'])
        self.assertEqual(updated_user.name, new_data['my_field_name'])
        self.assertEqual(updated_user.patronymic, new_data['my_field_patronymic'])
        self.assertEqual(updated_user.adress, new_data['my_field_address'])
        self.assertEqual(updated_user.phone_number, int(new_data['my_field_phone']))
        self.assertEqual(updated_user.age, int(new_data['my_field_age']))
        self.assertEqual(updated_user.sex, new_data['my_field_sex'])
        self.assertEqual(updated_user.flag_own_car, False)
        self.assertEqual(updated_user.flag_own_property, True)
        self.assertEqual(updated_user.month_income, float(new_data['my_field_month_income']))
        self.assertEqual(updated_user.count_children, int(new_data['my_field_count_children']))
        self.assertEqual(updated_user.education_type, new_data['my_field_education_type'])

    def test_update_client_with_errors(self):
        """Обновление клиента с некорректными данными"""
        incorrect_data = {
            'client_id': self.client1.pk,
            'my_field_passport': '',
            'my_field_surname': 'Петрова',
            'my_field_name': 'Анна',
            'my_field_patronymic': 'Павловна',
            'my_field_adress': 'Санкт-Петербург, Невский проспект, д. 10',
            'my_field_phone': '89997654321',
            'my_field_age': 'abcd',  # Некорректный возраст
            'my_field_sex': 'Женский',
            'my_field_flag_own_car': 'Нет',
            'my_flag_own_property': 'Да',
            'my_field_month_income': '-10000',  # Негативный доход
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }

        response = self.client.post(reverse('bank:update_client_view'), incorrect_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(errors)
        self.assertIn('passport', errors.keys())  # Ошибка паспорта
        self.assertIn('age', errors.keys())  # Ошибка возраста
        self.assertIn('income', errors.keys())  # Ошибка дохода

    def test_update_client_not_found(self):
        """Попробуем обновить несуществующего клиента"""
        wrong_id = 999999
        data = {
            'client_id': wrong_id,
            'my_field_passport': '9876547210',
            'my_field_surname': 'Петрова',
            'my_field_name': 'Анна',
            'my_field_patronymic': 'Павловна',
            'my_field_adress': 'Санкт-Петербург, Невский проспект, д. 10',
            'my_field_phone': '89997654321',
            'my_field_age': '35',
            'my_field_sex': 'Женский',
            'my_field_flag_own_car': 'Нет',
            'my_flag_own_property': 'Да',
            'my_field_month_income': '60000',
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }

        response = self.client.post(reverse('bank:update_client_view'), data)
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_content['success'])
        self.assertEqual(response_content['error'], f'Клиент {wrong_id} не найден.')

    def test_update_client_with_duplicate_passport(self):
        """Обновление клиента с дублирующимся номером паспорта"""
        duplicate_data = {
            'client_id': self.client1.pk,
            'my_field_passport': '9876543210',  # Дублируется номер паспорта другого клиента
            'my_field_surname': 'Иванова',
            'my_field_name': 'Мария',
            'my_field_patronymic': 'Владимировна',
            'my_field_adress': 'Самара, ул. Мира, д. 15',
            'my_field_phone': '89911122333',
            'my_field_age': '30',
            'my_field_sex': 'Женский',
            'my_field_flag_own_car': 'Да',
            'my_flag_own_property': 'Нет',
            'my_field_month_income': '55000',
            'my_field_count_children': '0',
            'my_field_education_type': 'Среднее специальное'
        }

        response = self.client.post(reverse('bank:update_client_view'), duplicate_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('passport', errors.keys())
        self.assertEqual(errors['passport'], 'Клиент с такими паспортными данными уже существует')

    def test_update_client_without_required_field(self):
        """Обновление клиента без обязательного поля"""
        incomplete_data = {
            'client_id': self.client1.pk,
            'my_field_passport': '9876540000',
            'my_field_surname': '',  # Обязательное поле пустое
            'my_field_name': 'Анна',
            'my_field_patronymic': 'Павловна',
            'my_field_adress': 'Санкт-Петербург, Невский проспект, д. 10',
            'my_field_phone': '+79997654321',
            'my_field_age': '35',
            'my_field_sex': 'Женский',
            'my_field_flag_own_car': 'Нет',
            'my_flag_own_property': 'Да',
            'my_field_month_income': '60000',
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }

        response = self.client.post(reverse('bank:update_client_view'), incomplete_data)
        errors = json.loads(response.content)['errors']

        self.assertEqual(response.status_code, 200)
        self.assertIn('surname', errors.keys())

    def test_add_new_client_successfully(self):
        """Проверяем успешное добавление нового клиента"""
        data = {
            'my_field_passport': '9876543290',
            'my_field_surname': 'Петров',
            'my_field_name': 'Петр',
            'my_field_patronymic': 'Петрович',
            'my_field_adress': 'Санкт-Петербург',
            'my_field_phone': '89001234568',
            'my_field_age': '35',
            'my_field_sex': 'Мужской',
            'my_field_flag_own_car': 'Да',
            'my_flag_own_property': 'Нет',
            'my_field_month_income': '60000',
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }
        response = self.client.post(reverse('bank:add_new_client'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertIsNotNone(Clients.objects.get(passport_serial_number='9876543210'))

    def test_add_existing_client(self):
        """Проверяем невозможность добавить клиента с уже существующими паспортными данными"""
        data = {
            'my_field_passport': '1234567890',  # Этот номер паспорта уже занят
            'my_field_surname': 'Иванов',
            'my_field_name': 'Иван',
            'my_field_patronymic': 'Иванович',
            'my_field_adress': 'Москва',
            'my_field_phone': '89001234567',
            'my_field_age': '30',
            'my_field_sex': 'Мужской',
            'my_field_flag_own_car': 'Нет',
            'my_flag_own_property': 'Да',
            'my_field_month_income': '50000',
            'my_field_count_children': '2',
            'my_field_education_type': 'Высшее'
        }
        response = self.client.post(reverse('bank:add_new_client'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('passport', response.json()['errors'])
        self.assertEqual(response.json()['errors']['passport'], 'Клиент с такими паспортными данными уже существует')

    def test_empty_required_field(self):
        """Проверяем попытку отправки формы с отсутствующими обязательными полями"""
        data = {
            'my_field_passport': '',  # Поле обязательно!
            'my_field_surname': 'Петров',
            'my_field_name': 'Петр',
            'my_field_patronymic': 'Петрович',
            'my_field_adress': 'Санкт-Петербург',
            'my_field_phone': '89001234568',
            'my_field_age': '35',
            'my_field_sex': 'Мужской',
            'my_field_flag_own_car': 'Да',
            'my_flag_own_property': 'Нет',
            'my_field_month_income': '60000',
            'my_field_count_children': '1',
            'my_field_education_type': 'Среднее специальное'
        }
        response = self.client.post(reverse('bank:add_new_client'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('passport', response.json()['errors'])
