$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function validateForm() {
        let isValid = true;

//        const credit_statement_Id = document.getElementById('credit_state_id');

        const credit_statement_Id = document.querySelector('#credit_state_id');

        const number_of_the_loan_agreementInput = document.getElementById('id_number_of_the_loan_agreement');
        if (isNaN(parseInt(number_of_the_loan_agreementInput.value)) || parseInt(number_of_the_loan_agreementInput.value) <= 0) {
            alert('Некорректное значение! Номер кредитного договора должен быть положительным целым числом.');
            isValid = false;
        }

        const credit_amountInput = document.getElementById('id_credit_amount');
        if (isNaN(parseInt(credit_amountInput.value)) || parseInt(credit_amountInput.value) <= 0) {
            alert('Некорректное значение! Сумма кредита должна быть положительным целым числом.');
            isValid = false;
        }

        const term_monthInput = document.getElementById('id_term_month');
        if (isNaN(parseInt(term_monthInput.value)) || parseInt(term_monthInput.value) <= 0) {
            alert('Некорректное значение! Срок кредита в месяцах должен быть положительным целым числом.');
            isValid = false;
        }

        const monthly_paymentInput = document.getElementById('id_monthly_payment');
        if (isNaN(parseInt(monthly_paymentInput.value)) || parseInt(monthly_paymentInput.value) <= 0) {
            alert('Некорректное значение! Ежемесячная выплата должна быть положительным целым числом.');
            isValid = false;
        }

        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        const loan_opening_dateInput = document.getElementById('id_loan_opening_date');
        if (!dateRegex.test(loan_opening_dateInput.value)) {
            alert('Некорректный формат даты! Дата должна быть в формате ГГГГ-ММ-ДД.');
            isValid = false;
        } else {
            // Разбираем дату на компоненты и проверяем их валидность
            const parts = loan_opening_dateInput.value.split('-');
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

        const repayment_statusInput = document.getElementById('id_repayment_status');
        if (repayment_statusInput.value != 'Да' && repayment_statusInput.value != 'Нет') {
            alert('Некорректное значение! Допустимы только значения Да или Нет".');
            isValid = false;
        }

        const loan_typeInput = document.getElementById('id_loan_type');
        if (isNaN(parseInt(loan_typeInput.value)) || parseFloat(loan_typeInput.value) <= 0) {
            alert('Некорректное значение! Регистрационный номер типа кредита должен быть положительным целым числом.');
            isValid = false;
        }

        const clientInput = document.getElementById('id_client');
        if (isNaN(clientInput.value) || !clientInput.value.match(/^\d{10}$/)) {
            alert('Некорректный формат паспорта! Пожалуйста, введите серию и номер паспорта в формате "XXXXXXXXXXX".');
            isValid = false;
        }
        return isValid;
    }


    // Обработчик события для кнопки "Сохранить изменения"
    $('.save_button').on('click', function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
        if (validateForm()) {
            // Собираем данные вручную
            const id = $('#credit_state_id').val();
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
            data.append('credit_state_id', id);
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