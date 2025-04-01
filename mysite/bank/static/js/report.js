document.addEventListener('DOMContentLoaded', function() {
    const createReportButton = document.querySelector('.create_report');
    var updateUrl = $('[data-update-url]').data('update-url');
    if (createReportButton) {

        createReportButton.addEventListener('click', function(event) {
            event.preventDefault();

            // Получаем значения отмеченных чекбоксов
            const checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            let selectedTables = [];

            checkedCheckboxes.forEach(function(checkbox) {
                selectedTables.push(checkbox.value);
            });
            console.log(selectedTables)
            // Отправляем данные на сервер методом POST
            fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tables: selectedTables
                })
            }).then(response => response.json())
              .then(data => {
                  console.log(data); // Логируем результат для отладки
                  alert("Ваш отчет был успешно сформирован.");
              })
              .catch(error => {
                  console.error('Ошибка:', error);
                  alert("Произошла ошибка при формировании отчета.");
              });
        });
    }
});

// Функция для получения CSRF-токена из cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}