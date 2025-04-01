$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    $('.delete-client').on('click', function(event) {
        event.preventDefault();

        const credit_type_id = $('#credit_type_id').val(); // Получение id
        const csrfToken = getCookie('csrftoken'); // Получение CSRF-токена
        fetch('/bank/delete_single_loan_type/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                credit_type_id: credit_type_id
            })
        }).then(response => {
            if (response.ok) {
                window.location.href = '/bank/credit_types';
            } else {
                alert('Ошибка при удалении типа кредита.');
            }
        });
    });


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        // Собираем данные вручную
        const credit_type_code = $('#id_credit_type_code').val();
        const credit_type_name = $('#id_credit_type_name').val();
        const credit_percent = $('#id_credit_percent').val().replace(',', '.');

        // Создаем объект для отправки
        const data = new URLSearchParams();
        if ( document.querySelector('#credit_type_id') != null){
            const credit_type_Id = $('#credit_type_id').val();
            data.append('credit_type_id', credit_type_Id);
        }
        data.append('my_field_credit_type_code', credit_type_code);
        data.append('my_field_credit_type_name', credit_type_name);
        data.append('my_field_credit_percent', credit_percent);
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
                alert('Изменения успешно сохранены');
                window.location.href = '/bank/credit_types/';
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
        })
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