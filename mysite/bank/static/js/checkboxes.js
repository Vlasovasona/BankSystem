var csrftoken = $('[name=csrfmiddlewaretoken]').val();
var deleteUrl = $('[data-delete-url]').data('delete-url');

$(document).ready(function() {
    console.log("Чекбокс изменился");
    // Изначально деактивируем кнопку удаления
    $('.delete-button').prop('disabled', true);

    // Отслеживаем изменения состояния чекбоксов
    $('input[name="table-checkbox"]').change(function() {
        // Проверяем наличие отмеченных чекбоксов
        var isChecked = $('input[name="table-checkbox"]:checked').length > 0;

        // Активируем/деактивируем кнопку в зависимости от наличия отмеченных чекбоксов
        $('.delete-button').prop('disabled', !isChecked);
    });

    // Обработчик нажатия на кнопку удаления
    $('.delete-button').click(function(e) {
        e.preventDefault();

        // Получаем идентификаторы всех отмеченных чекбоксов
        var selectedIds = $('input[name="table-checkbox"]:checked').map(function() {
            return $(this).val();
        }).get();

        // Отправляем данные на сервер
        $.ajax({
            url: deleteUrl, // Используем переменную с URL
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {
                'ids': JSON.stringify(selectedIds), // Преобразуем массив в строку
            },
            success: function(response) {
                // Удаляем строки с отмеченными чекбоксами из DOM
                $('input[name="table-checkbox"]:checked').closest('tr').remove();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});