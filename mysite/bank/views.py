# Вся логика приложения описывается здесь. Каждый обработчик получает HTTP-запрос, обрабатывает его и возвращает ответ

from django.shortcuts import render, get_object_or_404, redirect
from .models import Clients, CreditStatement, Credits
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, TemplateView


# Методы для работы с таблицей Clients

class ClientListView(ListView):
    queryset = Clients.objects.all()
    context_object_name = 'clients'
    paginate_by = 3
    template_name = 'bank/clients/list.html'

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

from .forms import ClientForm

# def edit_client(request, client_code):
#     client = get_object_or_404(Clients, client_code=client_code)
#     if request.method == 'POST':
#         form = ClientForm(request.POST, instance=client)
#         if form.is_valid():
#             form.save()
#             return redirect('client_detail', client_code=client_code)  # Переходим обратно на страницу клиента
#     else:
#         form = ClientForm(instance=client)
#
#     context = {
#         'form': form,
#         'client': client,
#     }
#     return render(request, 'bank/clients/edit_client.html', context)

# Методы для работы с таблицей Credits

class CreditsListView(ListView):
    queryset = Credits.objects.all()
    context_object_name = 'credits'
    paginate_by = 3
    template_name = 'bank/credits/list.html'

# Обязательно в параметрах указывать необходимы минимум для распознавания кортежа (в данном случае id)
def credit_detail(request, credit_code):
    """Представление подробной информации о конкретном кредите.
    :param request: HTTP-запрос.
    :param credit_code: Код кредита.
    :return: Возвращает HTML-шаблон с контекстом, содержащим детали клиента. """
    client = get_object_or_404(Clients, credit_code=credit_code)
    context = {
        'credit': credit,
    }
    return render(request, 'bank/credits/detail.html', context)

