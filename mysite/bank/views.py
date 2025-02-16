# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404
from .models import Clients
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

class ClientListView(ListView):
    queryset = Clients.objects.all()
    context_object_name = 'clients'
    paginate_by = 3
    template_name = 'bank/clients/list.html'

# def clients_list(request):
#     """Получение списка всех клиентов из базы данных.
#     :param request: HTTP-запрос.
#     :return: Возвращает HTML-шаблон с контекстом, содержащим список клиентов."""
#     clients = Clients.objects.all()
#
#     paginator = Paginator(clients, 3)
#     page = request.GET.get('page')
#     try:
#         clients = paginator.page(page)
#     except PageNotAnInteger:
#         # if page not integer, returns first page
#         clients = paginator.page(1)
#     except EmptyPage:
#         # if number of page is more than count, returns last one.
#         clients = paginator.page(paginator.num_pages)
#
#     return render(request, 'bank/clients/list.html', {'clients': clients})

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def client_detail(request, client_code):
    """Представление подробной информации о конкретном клиенте.
    :param request: HTTP-запрос.
    :param client_code: Код клиента.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, client_code=client_code)
    context = {
        'client': client,
    }
    return render(request, 'bank/clients/detail.html', context)