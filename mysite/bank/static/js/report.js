document.addEventListener('DOMContentLoaded', function () {
    const createReportButton = document.querySelector('.create_report');
    var updateUrl = $('[data-update-url]').data('update-url');

    if (createReportButton) {
        createReportButton.addEventListener('click', async function (event) {
            event.preventDefault();

            // Получаем значения отмеченных чекбоксов
            const checkedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            let selectedTables = [];

            checkedCheckboxes.forEach((checkbox) => {
                selectedTables.push(checkbox.value);
            });

            if (selectedTables.length === 0) {
                alert("Ошибка: Не отмечено ни одного элемента!");
                return; // Прекращаем дальнейшее выполнение обработки формы
            }

            // Отправляем данные на сервер методом POST
            const response = await fetch(updateUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ tables: selectedTables }),
            });

            if (!response.ok) {
                throw new Error(`Network response was not ok (${response.status})`);
            }

            // Получаем двоичные данные (blob) и инициируем скачивание
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'report.pdf';
            document.body.appendChild(link);
            link.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(link);

            alert("Ваш отчет был успешно сформирован.");
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