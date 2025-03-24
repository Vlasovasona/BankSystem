from django.contrib import admin
from django.urls import path
from . import views


app_name = 'bank'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='clients_list'),
    path('clients/<int:client_code>/', views.client_detail, name='client_detail'),
    path('clients/', views.ClientListView.as_view(), name='clients_list_select'),

    # path('credits/<int:credit_code>/', views.credit_detail, name='credit_detail'),
    # path('credits/', views.CreditsListView.as_view(), name='credit_list'),
    #
    # path('credit_types/<int:credit_type_code>/', views.credit_type_detail, name='credit_type_detail'),
    # path('credit_types/', views.CreditTypesListView.as_view(), name='credit_types_list'),
    #
    # path('deposits/<int:deposit_code>/', views.deposit_detail, name='deposit_detail'),
    # path('deposits/', views.DepositsListView.as_view(), name='deposit_list'),
    #
    # path('deposit_types/<int:deposit_type_code>/', views.deposit_type_detail, name='deposit_type_detail'),
    # path('deposit_types/', views.DepositTypesListView.as_view(), name='deposit_types_list'),
    #
    # path('statement_of_deposits/<int:deposit_closing_number>/', views.statement_of_deposits_detail, name='statement_of_deposits_detail'),
    # path('statement_of_deposits/', views.StatementOfDepositsListView.as_view(), name='statement_of_deposits_list'),
    #
    # path('credit_statement/<int:loan_repayment_number>/', views.credit_statement_detail, name='credit_statement_detail'),
    # path('credit_statement/', views.CreditStatementListView.as_view(), name='credit_statement_list'),
    #
    #
    # path('clients/search', views.search_clients, name='search_clients'),
]

