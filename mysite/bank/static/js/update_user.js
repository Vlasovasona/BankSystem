$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    $('.delete-client').on('click', function(event) {
        event.preventDefault();

        const username = $('#my_field_login').val(); // Получение id клиента
        const csrfToken = getCookie('csrftoken'); // Получение CSRF-токена

        fetch('/bank/delete_single_user/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'my_field_login': username,
                'csrfmiddlewaretoken': csrfToken // Передавайте CSRF токен в JSON
            })
        }).then(response => {
            if (response.ok) {
                 window.location.href = '/bank/users';
            } else {
                alert('Ошибка при удалении пользователя.');
            }
        });
    });

    function validateForm() {
        let isValid = true;

        const userId = document.querySelector('#user_id');
        const surnameInput = document.getElementById('id_last_name');
        if (!(surnameInput.value.trim().length === 0 || !surnameInput.value.match(/^[А-ЯЁа-яё ]+$/u))) {
            alert('Некорректный формат фамилии! Фамилия должна состоять только из букв".');
            isValid = false;
        }

        const nameInput = document.getElementById('id_name');
        if (!(nameInput.value.trim().length === 0 || !nameInput.value.match(/^[А-ЯЁа-яё ]+$/u))) {
            alert('Некорректный формат имени! Имя должно состоять только из букв".');
            isValid = false;
        }

        const emailInput = document.getElementById('id_email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!(emailInput.value.trim().length === 0 || emailRegex.test(emailInput.value))) {
            alert('Некорректный формат электронной почты!');
            isValid = false;
        }

        const is_staffInput = document.getElementById('id_is_staff');
        if (is_staffInput.value != 'Да' && is_staffInput.value != 'Нет') {
            alert('Некорректное значение! Допустимы только значения Да или Нет".');
            isValid = false;
        }

        const is_activeInput = document.getElementById('id_is_active');
        if (is_activeInput.value != 'Да' && is_activeInput.value != 'Нет') {
            alert('Некорректное значение! Допустимы только значения Да или Нет".');
            isValid = false;
        }

        return isValid;
    }


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault();
        if (validateForm()) {
            const username = $('#my_field_login').val();
            const last_name = $('#id_last_name').val();
            const first_name = $('#id_name').val();
            const email = $('#id_email').val();
            const is_staff = $('#id_is_staff').val();
            const is_active = $('#id_is_active').val();

            // Создаем объект для отправки
            const data = new URLSearchParams();
            data.append('my_field_login', username);
            data.append('my_field_last_name', last_name);
            data.append('my_field_name', first_name);
            data.append('my_field_email', email);
            data.append('my_field_is_staff', is_staff);
            data.append('my_field_is_active', is_active);

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