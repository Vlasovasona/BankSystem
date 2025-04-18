$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var analysisUrl = $('[data-analysis-url]').data('analysis-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function checkFields() {
        let fields = [
            document.querySelector('#id_client'),
            document.querySelector('#id_number_of_the_loan_agreement'),
            document.querySelector('#id_credit_amount'),
            document.querySelector('#id_term_month'),
            document.querySelector('#id_monthly_payment'),
            document.querySelector('#id_loan_opening_date'),
            document.querySelector('#id_loan_type')
        ];

        // Фильтруем поля, которые пусты
        let emptyFields = fields.filter(field => field.value.trim() === '');

        // Если есть хотя бы одно пустое поле, отключаем кнопку
        if (emptyFields.length > 0) {
            document.querySelector('.analysis-button').disabled = true;
        } else {
            document.querySelector('.analysis-button').disabled = false;
        }
    }

    // Обработчики событий для всех полей
    let inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            checkFields(); // Проверка после любого изменения
        });
    });

    // Первичная проверка при загрузке страницы
    checkFields();

    function create_data() {
        const number_of_the_loan_agreement = $('#id_number_of_the_loan_agreement').val();
        const credit_amount = $('#id_credit_amount').val();
        const term_month = $('#id_term_month').val();
        const monthly_payment = $('#id_monthly_payment').val();
        const loan_opening_date = $('#id_loan_opening_date').val();
        const repayment_status = $('#id_repayment_status').val();
        const loan_type = $('#id_loan_type').val();
        const client = $('#id_client').val();

        // Создаем объект для отправки
        const data = new URLSearchParams();
        if ( document.querySelector('#credit_state_id') != null){
            const id = $('#credit_state_id').val();
            data.append('credit_state_id', id);
        }
        data.append('my_field_number_of_the_loan_agreement', number_of_the_loan_agreement);
        data.append('my_field_credit_amount', credit_amount);
        data.append('my_term_month', term_month);
        data.append('my_field_monthly_payment', monthly_payment);
        data.append('my_field_loan_opening_date', loan_opening_date);
        data.append('my_field_repayment_status', repayment_status);
        data.append('my_field_loan_type', loan_type);
        data.append('my_field_client', client);

        // Добавляем csrf-token
        data.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());
        return data
    }

    $('.analysis-button').on('click', function(event) {
        document.querySelector('.analysis-button').disabled = true;
        event.preventDefault();

        // Отправка данных на сервер
        fetch(analysisUrl, {
            method: 'POST',
            body: create_data()
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
            return response.json(); // Only proceed to the next `.then()` if the response is OK
        })
        .then(data => {
            console.log('Server Response:', data);
            if (data && data.success) {
                alert('Система одобрила заявку. Она автоматически добавлена в ведомость');
            } else {
                const errorElements = document.querySelectorAll('.error-message');
                errorElements.forEach(element => {
                    element.textContent = '';
                });

                if (data.errors) {
                    for (const key in data.errors) {
                        const errorMessage = data.errors[key];
                        const errorElement = document.getElementById(`${key}-error`);
                        if (errorElement) {
                            errorElement.textContent = errorMessage;
                        }
                    }
                } else {
                      let modal = document.getElementById('confirmation-modal');
                      //let yesBtn = document.getElementById('save_button');
                      let noBtn = document.getElementById('confirm-no');
                      let modalText = document.getElementById('modal-text');

                      modalText.innerText = data.error;
                      modal.style.display = 'block';

                      // Обработчики нажатия кнопок
                      noBtn.onclick = () => {
                          modal.style.display = 'none';
                          window.location.href = '/bank/application_page/';
                      };
                }
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
        });
    });


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        let modal = document.getElementById('confirmation-modal');
        if (modal.style.display = 'block') {
            modal.style.display = 'none';
        }

        // Отправка данных на сервер
        fetch(updateUrl, {
            method: 'POST',
            body: create_data() // отправляем данные
        })
        .then(response => response.json()) // получаем JSON ответ
        .then(data => {
            console.log('Server Response:', data);
            if (data && data.success) {
                alert('Изменения успешно сохранены');
                window.location.href = '/bank/application_page/';
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