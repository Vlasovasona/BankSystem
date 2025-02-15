# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404
from .models import Clients

def clients_list(request):
    """Получение списка всех клиентов из базы данных.
    :param request: HTTP-запрос.
    :return: Возвращает HTML-шаблон с контекстом, содержащим список клиентов."""
    clients = Clients.objects.all()
    return render(request, 'bank/clients/list.html', {'clients': clients})

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def client_detail(request, unique_code):
    """ Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :param unique_code: Уникальный код клиента.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, client_code = unique_code)
    return render(request, 'bank/clients/detail.html')