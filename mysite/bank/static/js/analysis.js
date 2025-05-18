$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var analysisUrl = $('[data-analysis-url]').data('analysis-url');
    var clients_search_Url = $('[data-clients-url]').data('clients-url');
    var types_search_Url = $('[data-types-url]').data('types-url');
    var create_number_Url = $('[data-create-number-url]').data('create-number-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function checkFields() {
        let fields = [
            document.querySelector('#id_client'),
            document.querySelector('#id_number_of_the_loan_agreement'),
            document.querySelector('#id_credit_amount'),
            document.querySelector('#id_term_month'),
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

    function checkFields_for_number_of_the_loan() {
        let fields = [
            document.querySelector('#id_client'),
            document.querySelector('#id_loan_type')
        ];

        // Фильтруем поля, которые пусты
        let emptyFields = fields.filter(field => field.value.trim() === '');

        // Если все поля заполнены
        if (emptyFields.length === 0) {
            $.ajax({
                url: create_number_Url,
                type: "GET",
                data: create_data_for_loan_number(),   // Используем возвращаемый объект
                success: function(response) {
                    console.log('Received response:', response);

                    if (response && typeof response.number_of_agreement === 'string') {
                        $('#id_number_of_the_loan_agreement').val(response.number_of_agreement);
                    } else {
                        console.warn("Unexpected response format:", response);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching suggestions:", xhr.responseText);
                }
            });
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
        data.append('my_field_loan_type', loan_type);
        data.append('my_field_client', client);

        // Добавляем csrf-token
        data.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());
        return data
    }

    function create_data_for_loan_number() {
        const my_field_client = document.querySelector('#id_client').value;
        const my_field_loan_type = document.querySelector('#id_loan_type').value;

        return { my_field_client, my_field_loan_type };
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
            return response.json();
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
                      let noBtn = document.getElementById('confirm-no');
                      let modalText = document.getElementById('modal-text');

                      modalText.innerText = data.error;
                      modal.style.display = 'block';

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
                alert(`Изменения успешно сохранены. ${data.message}`);
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

    $('#id_client').on('input', function(e) {
        const searchQuery = $(this).val().trim();

        if(searchQuery.length >= 3) { // начинаем искать после трех символов
            $.ajax({
                url: clients_search_Url,
                type: "GET",
                data: {'q': searchQuery},
                success: function(response) {
                    console.log('Received response:', response);
                    if (response && Array.isArray(response.clients)) {
                        console.log("here1")
                        showSuggestions(response.clients);
                    } else {
                        console.log("here2")
                        console.warn("Unexpected response format:", response);
                        showSuggestions([]);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching suggestions:", xhr.responseText);
                }
            });
        } else {
            hideSuggestions();
        }
    });

    // Скрываем подсказки при клике вне области
    $('body').on('click', function(e) {
        if ($(e.target).closest('#suggestions-list').length === 0 &&
            $(e.target).attr('id') !== 'id_client') {
            hideSuggestions();
        }
    });

    function showSuggestions(clients) {
        const listEl = $('#suggestions-list');
        listEl.empty(); // очищаем
        clients.forEach(function(client) {
            const li = $('<li></li>')
                .text(client.surname + ' ' + client.name + ' ' + client.patronymic + ', ' + client.passport)
                .data('passport', client.passport);
            listEl.append(li);
        });
        listEl.show();

        // Обрабатываем клик по варианту выбора
        listEl.find('li').on('click', function() {
            const selectedPassport = $(this).data('passport');
            $('#id_client').val(selectedPassport); // подставляем паспорт в input
            hideSuggestions();
            checkFields_for_number_of_the_loan();
        });
    }

    // Скрытие списка предложений
    function hideSuggestions() {
        $('#suggestions-list').hide();
    }

    $('#id_loan_type').on('input', function(e) {
        const searchQuery = $(this).val().trim();

        if(searchQuery.length >= 3) { // начинаем искать после трех символов
            $.ajax({
                url: types_search_Url,
                type: "GET",
                data: {'q': searchQuery},
                success: function(response) {
                    console.log('Received response:', response);
                    if (response && Array.isArray(response.types)) {
                        show_types_Suggestions(response.types);
                    } else {
                        console.warn("Unexpected response format:", response);
                        show_types_Suggestions([]);
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching suggestions:", xhr.responseText);
                }
            });
        } else {
            hide_types_Suggestions();
        }
    });

    // Скрываем подсказки при клике вне области
    $('body').on('click', function(e) {
        if ($(e.target).closest('#suggestions-list_type').length === 0 &&
            $(e.target).attr('id') !== 'id_loan_type') {
            hide_types_Suggestions();
        }
    });

    function show_types_Suggestions(types) {
        const listEl = $('#suggestions-list_type');
        listEl.empty(); // очищаем
        types.forEach(function(type) {
            const li = $('<li></li>')
                .text(type.name + ', ' + type.registration_number)
                .data('registration_number', type.registration_number);
            listEl.append(li);
        });
        listEl.show();

        // Обрабатываем клик по варианту выбора
        listEl.find('li').on('click', function() {
            const selectedRegistration_number = $(this).data('registration_number');
            $('#id_loan_type').val(selectedRegistration_number); // подставляем паспорт в input
            hide_types_Suggestions();
            checkFields_for_number_of_the_loan();
        });
    }

    // Скрытие списка предложений
    function hide_types_Suggestions() {
        $('#suggestions-list_type').hide();
    }

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