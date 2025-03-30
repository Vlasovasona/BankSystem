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

    function validateForm() {
        let isValid = true;

//        const clientId = document.getElementById('client_id');
        const clientId = document.querySelector('#client_id');
        const surnameInput = document.getElementById('id_surname');
        if (!surnameInput.value.match(/^[А-ЯЁа-яё ]+$/u)) {
            alert('Некорректный формат фамилии! Фамилия должна состоять только из букв".');
            isValid = false;
        }

        const nameInput = document.getElementById('id_name');
        if (!nameInput.value.match(/^[А-ЯЁа-яё ]+$/u)) {
            alert('Некорректный формат имени! Имя должно состоять только из букв".');
            isValid = false;
        }

        const patronymicInput = document.getElementById('id_patronymic');
        if (!patronymicInput.value.match(/^[А-ЯЁа-яё ]+$/u)) {
            alert('Некорректный формат отчества! Отчество должно состоять только из букв".');
            isValid = false;
        }

        const genderInput = document.getElementById('id_sex');
        if (genderInput.value != 'Мужской' && genderInput.value != 'Женский') {
            alert('Некорректно указан пол клиента! Допустимы только значения Мужской или Женский".');
            isValid = false;
        }

        const carInput = document.getElementById('id_flag_own_car');
        if (carInput.value != 'Да' && carInput.value != 'Нет') {
            alert('Некорректное значение! Допустимы только значения Да или Нет".');
            isValid = false;
        }

        const propertyInput = document.getElementById('id_flag_own_property');
        if (propertyInput.value != 'Да' && propertyInput.value != 'Нет') {
            alert('Некорректное значение! Допустимы только значения Да или Нет".');
            isValid = false;
        }

        const incomeInput = document.getElementById('id_month_income');
        if (isNaN(parseFloat(incomeInput.value)) || parseFloat(incomeInput.value) <= 0) {
            alert('Некорректное значение дохода! Допустимы только числовые положительные значения".');
            isValid = false;
        }

        // Проверка паспорта
        const passportInput = document.getElementById('my_field_passport');
        if (isNaN(passportInput.value) || !passportInput.value.match(/^\d{10}$/)) {
            alert('Некорректный формат паспорта! Пожалуйста, введите серию и номер паспорта в формате "XXXXXXXXXXX".');
            isValid = false;
        }

        // Проверка возраста
        const ageInput = document.getElementById('id_age');
        if (isNaN(ageInput.value) || parseInt(ageInput.value) <= 0 || parseInt(ageInput.value) > 110) {
            alert('Некорректный возраст! Пожалуйста, укажите правильный возраст.');
            isValid = false;
        }

        const childrenInput = document.getElementById('id_count_children');
        if (isNaN(childrenInput.value) || parseInt(childrenInput.value) < 0 || parseInt(childrenInput.value) >= 20) {
            alert('Некорректное значение! Количество детей может быть от 0 до 20.');
            isValid = false;
        }

        const educationInput = document.getElementById('id_education_type');
        if (educationInput.value != "Высшее" && educationInput.value != "Среднее специальное") {
            alert('Некорректное значение! Допустимые значения: Высшее, Среднее специальное');
            isValid = false;
        }

        // Проверка номера телефона
        const phoneInput = document.getElementById('id_phone');
        if (isNaN(phoneInput.value) || !phoneInput.value.match(/^(\+7|7|8)[\d\s\-]{10,15}$/)) {
            alert('Некорректный формат номера телефона!');
            isValid = false;
        }

        return isValid;
    }


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        if (validateForm()) {
            // Собираем данные вручную

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
            if ( document.querySelector('#client_id') != null){
                const clientId = $('#client_id').val();
                data.append('client_id', clientId);
            }

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
            .then(response => response.json())
            .then(data => {
                console.log('Server Response:', data);
                if (data && data.success) {
                    alert('Изменения успешно сохранены!');
                } else {
                    alert('Произошла ошибка при сохранении изменений: ' + (data.error || 'Неизвестная ошибка.'));
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                alert('Произошла ошибка при отправке данных на сервер.');
            });
        }
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