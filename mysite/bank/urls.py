from django.contrib import admin
from django.urls import path
from . import views

app_name = 'bank'

urlpatterns = [
    # path('', views.clients_list, name='clients_list'),
    path('', views.ClientListView.as_view(), name='clients_list'),
    path('<int:client_code>/', views.client_detail, name='client_detail'),
]