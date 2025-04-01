$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    $('.delete-client').on('click', function(event) {
        event.preventDefault();

        const pay_id = $('#pay_id').val(); // Получение id клиента
        const csrfToken = getCookie('csrftoken'); // Получение CSRF-токена

        fetch('/bank/delete_single_payroll/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pay_id: pay_id // Передача id в теле запроса
            })
        }).then(response => {
            if (response.ok) {
                 window.location.href = '/bank/payroll';
            } else {
                alert('Ошибка при удалении платежа.');
            }
        });
    });


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        // Собираем данные вручную
        const loan = $('#id_loan').val();
        const date = $('#id_payment_date').val();
        const status = $('#id_payment_status').val();

        // Создаем объект для отправки
        const data = new URLSearchParams();
        if ( document.querySelector('#pay_id') != null){
            const payId = $('#pay_id').val();
            data.append('pay_id', payId);
        }
        data.append('my_field_loan', loan);
        data.append('my_field_payment_date', date);
        data.append('my_field_payment_status', status);

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
                window.location.href = '/bank/payroll/';
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