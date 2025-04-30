$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    $('.delete-client').on('click', function(event) {
        event.preventDefault();

        const clientId = $('#client_id').val(); // Получение id клиента
        const csrfToken = getCookie('csrftoken'); // Получение CSRF-токена

        fetch('/bank/delete_single_client/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                client_id: clientId // Передача client_id в теле запроса
            })
        }).then(response => {
            if (response.ok) {
                 window.location.href = '/bank/clients';
            } else {
                alert('Ошибка при удалении клиента.');
            }
        });
    });



    $('.save_button').on('click', function(event) { // Начало функции-обработчика
        event.preventDefault(); // предотвращаем стандартное поведение формы
        // Сбор данных из полей формы
        const passport = $('#my_field_passport').val();
        const surname = $('#id_surname').val();
        const name = $('#id_name').val();
        const patronymic = $('#id_patronymic').val();
        const address = $('#id_adress').val();
        const phoneNumber = $('#id_phone').val();
        const age = $('#id_age').val();
        const sex = $('#id_sex').val();
        const flagOwnCar = $('#id_flag_own_car').val();
        const flagOwnProperty = $('#id_flag_own_property').val();
        const monthIncome = $('#id_month_income').val();
        const countChildren = $('#id_count_children').val();
        const educationType = $('#id_education_type').val();

        // Создаем объект для отправки
        const data = new URLSearchParams();
        if (document.querySelector('#client_id') !== null) {
            const clientId = $('#client_id').val();
            data.append('client_id', clientId);
        }

        // Добавление данных в форму отправки
        data.append('my_field_passport', passport);
        data.append('my_field_surname', surname);
        data.append('my_field_name', name);
        data.append('my_field_patronymic', patronymic);
        data.append('my_field_adress', address);
        data.append('my_field_phone', phoneNumber);
        data.append('my_field_age', age);
        data.append('my_field_sex', sex);
        data.append('my_field_flag_own_car', flagOwnCar);
        data.append('my_flag_own_property', flagOwnProperty);
        data.append('my_field_month_income', monthIncome);
        data.append('my_field_count_children', countChildren);
        data.append('my_field_education_type', educationType);

        // Добавляем csrf-token
        data.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());

        // Отправка данных на сервер
        fetch(updateUrl, {
            method: 'POST',
            body: data // отправляем данные
        })
        .then(response => response.json()) // получаем JSON ответ
        .then(data => {
            console.log('Server Response:', data);
            if (data && data.success) {
                alert('Изменения успешно сохранены!');
            } else {
                // Очистка предыдущих ошибок
                const errorElements = document.querySelectorAll('.error-message');
                errorElements.forEach(element => {
                    element.textContent = ''; // очищаем предыдущие сообщения об ошибках
                });

                if (data.errors) {
                    // Обработка ошибок
                    for (const key in data.errors) {
                        const errorMessage = data.errors[key];
                        const errorElement = document.getElementById(`${key}-error`);
                        if (errorElement) {
                            errorElement.textContent = errorMessage; // Устанавливаем текст ошибки
                        }
                    }
                } else {
                    alert('Произошла ошибка при сохранении изменений: ' + (data.error || 'Неизвестная ошибка.'));
                }
            }
        }) // Закрывающая скобка после then
        .catch(error => {
            console.error('Fetch Error:', error);
            alert('Произошла ошибка при отправке данных на сервер.');
        });
    });
});


// Функция для получения CSRF-токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}