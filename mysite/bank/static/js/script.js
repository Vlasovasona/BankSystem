function handleChange(select) {
    var url = select.value; // Получаем значение выбранного элемента
    if (url !== '') { // Если выбрано что-то кроме пустого значения
        window.location.href = url; // Переходим по выбранной ссылке
    }
}

