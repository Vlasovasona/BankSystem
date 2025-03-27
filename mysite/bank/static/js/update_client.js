//// Получаем URL из HTML-атрибута или переменной
//    var updateUrl = $('[data-update-url]').data('update-url');
//    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
//
//$(document).ready(function() {
//    // Обработчик события для кнопки "Сохранить изменения"
//    $('.save_button').on('click', function(event) {
//        event.preventDefault(); // предотвращаем стандартное поведение формы
//
//        // Функция для проверки значений ввода
//
//
//        // Получение всех данных из формы
//        var formData = {
//            client_id: $('#client_id').val(),
//            passport_serial_number: $('#my_field_passport').val(),
//            surname: $('#id_surname').val(),
//            name: $('#id_name').val(),
//            patronymic: $('#id_patronymic').val(),
//            adress: $('#id_adress').val(),
//            phone_number: $('#id_phone').val(),
//            age: $('#id_age').val(),
//            sex: $('#id_sex').val(),
//            flag_own_car: $('#id_flag_own_car').val() === 'Да',   // преобразуем в булево
//            flag_own_property: $('#id_flag_own_property').val() === 'Да', // преобразуем в булево
//            month_income: $('#id_month_income').val(),
//            count_children: $('#id_count_children').val(),
//            education_type: $('#id_education_type').val()
//        };
//
//        // Пример вывода в консоль
//        console.log(formData);
//
//        if (validateForm()) {
////            const form = $('form')[0]; // Получаем первый элемент формы
////            const formData = new FormData(form);
////            for (let [key, value] of formData.entries()) {
////                console.log(`${key}: ${value}`);
////            }
//
//            fetch(updateUrl, {
//                method: 'POST',
//                headers: {
//                    'X-CSRFToken': csrftoken,
//                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
//                },
//                body: new URLSearchParams(formData).toString()
//            })
//            .then(response => response.json())
//            .then(data => {
//                console.log('Server Response:', data);
//                if (data && data.success) {
//                    alert('Изменения успешно сохранены!');
//                } else {
//                    alert('Произошла ошибка 1 при сохранении изменений.');
//                }
//            })
//            .catch(error => {
//                console.error('Fetch Error:', error);
//                alert('Произошла ошибка 2 при сохранении изменений.');
//            });
//        }
//
//        // Отправка данных на сервер через AJAX
////        $.ajax({
////            url: $('div[data-update-url]').data('update-url'), // URL для отправки
////            type: 'POST',
////            data: formData,
////            success: function(response) {
////                // Обработка успешного ответа
////                console.log('Данные успешно отправлены:', response);
////                // Тут можно добавить дальнейшие действия, например, сообщение об успешном сохранении
////            },
////            error: function(xhr, status, error) {
////                // Обработка ошибок
////                console.error('Ошибка при отправке данных:', error);
////            }
////        });
//    });
//});
$(document).ready(function() {
    // Получаем URL из HTML-атрибута или переменной
    var updateUrl = $('[data-update-url]').data('update-url');
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();

    function validateForm() {
        let isValid = true;
        console.log("Скрипт выполняется");

        const clientId = document.getElementById('client_id');
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
            const clientId = $('#client_id').val();
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
            data.append('client_id', clientId);
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