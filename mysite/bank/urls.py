from django.contrib import admin
from django.urls import path
from . import views


app_name = 'bank'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='clients_list'),
    path('clients/<int:id>/', views.client_detail, name='client_detail'),
    path('clients/', views.ClientListView.as_view(), name='clients_list_select'),
    path('clients/search', views.search_clients, name='search_clients'),

    path('credit_types/<int:id>/', views.credit_type_detail, name='credit_type_detail'),
    path('credit_types/', views.CreditTypesListView.as_view(), name='credit_types_list'),

    path('credit_statement/<int:id>/', views.credit_statement_detail, name='credit_statement_detail'),
    path('credit_statement/', views.CreditStatementListView.as_view(), name='credit_statement_list'),

    path('payroll/<int:id>/', views.payroll_detail, name='payroll_detail'),
    path('payroll/', views.PayrollListView.as_view(), name='payroll_list'),

    path('delete-clients/', views.delete_clients, name='delete_clients'),
    path('delete-credit-type/', views.delete_credit_type, name='delete-credit-type'),
    path('delete-payroll/', views.delete_payroll, name='delete-payroll'),
    path('delete-credit-statement/', views.delete_credit_statement, name='delete-credit-statement'),

    path('update-clients/', views.update_client_view, name='update_client_view'),
    path('update-credit-type/', views.update_loan_type, name='update-credit-type'),
    # path('update-payroll/', views.delete_payroll, name='delete-payroll'),
    # path('update-credit-statement/', views.delete_credit_statement, name='delete-credit-statement'),
]
