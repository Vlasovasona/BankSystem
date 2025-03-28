from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include


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
    path('update-payroll/', views.update_payroll, name='update-payroll'),
    path('update-credit-statement/', views.update_credit_statement, name='update-credit-statement'),

    path('clients/add_new', views.client_add_detail, name='client_add_detail'),
    path('credit_types/add_new', views.credit_types_add_detail, name='credit_types_add_detail'),
    path('credit_statement/add_new', views.credit_statement_add_detail, name='credit_statement_add_detail'),
    path('payroll/add_new', views.payroll_add_detail, name='payroll_add_detail'),

    path('add-clients/', views.add_new_client, name='add_new_client'),
    path('add-credit-type/', views.add_new_loan_type, name='add_new_credit_type'),
    path('add-payroll/', views.add_new_payroll, name='add_new_payroll'),
    path('add-credit-statement/', views.add_new_credit_statement, name='add_new_credit_statement'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

]
