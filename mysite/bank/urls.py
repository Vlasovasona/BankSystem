from django.contrib import admin
from django.urls import path
from . import views


app_name = 'bank'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='clients_list'),
    path('clients/<int:client_code>/', views.client_detail, name='client_detail'),
    path('clients/', views.ClientListView.as_view(), name='clients_list_select'),

    path('credits/<int:credit_code>/', views.credit_detail, name='credit_detail'),
    path('credits/', views.CreditsListView.as_view(), name='credit_list'),
]