$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function validateForm() {
        let isValid = true;

//        const paytId = document.getElementById('pay_id');
        const paytId = document.querySelector('#pay_id');

        const loanInput = document.getElementById('id_loan');
        if (isNaN(parseInt(loanInput.value)) || parseFloat(loanInput.value) <= 0) {
            alert('Некорректное значение регистрационного номера кредита! Допустимы только числовые положительные значения".');
            isValid = false;
        }

        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        const pay_date_Input = document.getElementById('id_payment_date');
        // Проверка соответствия введённой строки формату даты
        if (!dateRegex.test(pay_date_Input.value)) {
            alert('Некорректный формат даты! Дата должна быть в формате ГГГГ-ММ-ДД.');
            isValid = false;
        } else {
            // Разбираем дату на компоненты и проверяем их валидность
            const parts = pay_date_Input.value.split('-');
            const year = parseInt(parts[0], 10);  // Год
            const month = parseInt(parts[1], 10); // Месяц (1-12)
            const day = parseInt(parts[2], 10);   // День (1-31)

            // Проверка диапазонов значений года, месяца и дня
            if (year < 1900 || year > 2100) {  // Ограничиваем диапазон годов
                alert('Год должен быть между 1900 и 2100.');
                isValid = false;
            } else if (month < 1 || month > 12) {  // Месяцы должны быть от 1 до 12
                alert('Месяц должен быть от 1 до 12.');
                isValid = false;
            } else if (day < 1 || day > 31) {  // Дни должны быть от 1 до 31
                alert('День должен быть от 1 до 31.');
                isValid = false;
            } else {
                // Дополнительно можно проверить, соответствует ли день количеству дней в месяце
                const daysInMonth = new Date(year, month - 1, 0).getDate();  // Получаем количество дней в месяце
                if (day > daysInMonth) {
                    alert(`Неверная дата! В месяце ${month} всего ${daysInMonth} дней.`);
                    isValid = false;
                }
            }
        }

        const statusInput = document.getElementById('id_payment_status');
        // Проверка на соответствие числу в диапазоне от 0 до 5 или строкам "X" и "C"
        if ((statusInput.value >= 0 && statusInput.value <= 5) ||
            statusInput.value === "X" ||
            statusInput.value === "C") {
            // Значение корректно
        } else {
            alert('Некорректное значение статуса платежа! Допустимые значения: от 0 до 5, "X" или "C".');
            isValid = false;
        }

        return isValid;
    }


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        if (validateForm()) {
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