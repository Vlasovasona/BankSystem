$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function validateForm() {
        let isValid = true;

//        const clientId = document.getElementById('credit_type_id');
        const clientId = document.querySelector('#credit_type_id');


        const nameInput = document.getElementById('id_credit_type_name');
        if (!nameInput.value.match(/^[А-ЯЁа-яё ]+$/u)) {
            alert('Некорректный формат названия кредита! Оно должно состоять только из букв".');
            isValid = false;
        }

        const credit_type_code_Input = document.getElementById('id_credit_type_code');
        if (isNaN(parseInt(credit_type_code_Input.value)) || parseFloat(credit_type_code_Input.value) <= 0) {
            alert('Некорректное значение регистрационного номера кредита! Допустимы только числовые положительные значения".');
            isValid = false;
        }

        const percentInput = document.getElementById('id_credit_percent');
        if (isNaN(parseFloat(percentInput.value.replace(',', '.'))) ||
            parseFloat(percentInput.value.replace(',', '.')) <= 0 ||
            parseFloat(percentInput.value.replace(',', '.')) > 100) {
            alert('Некорректное значение процентной ставки! Пожалуйста, укажите положительное число.');
            isValid = false;
        }

        return isValid;
    }


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        if (validateForm()) {
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