# Регистрация моделей для добавления их в систему администрирования Django
from django.contrib import admin
from .models import AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser
from .models import AuthUserGroups, AuthUserUserPermissions, Clients, CreditStatement
from .models import CreditType, Credits, DepositTypes, Deposits, DescriptiveStatistics
from .models import DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession, StatementOfDeposits, Statistics



admin.site.register(AuthGroup)
admin.site.register(AuthGroupPermissions)
admin.site.register(AuthPermission)
admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(Clients)
admin.site.register(CreditStatement)
admin.site.register(CreditType)
admin.site.register(Credits)
admin.site.register(DepositTypes)
admin.site.register(Deposits)
admin.site.register(DescriptiveStatistics)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)
admin.site.register(StatementOfDeposits)
admin.site.register(Statistics)

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    search_fields = ('familia', 'name', 'otchestvo')
    list_display = ('familia', 'name', 'otchestvo', 'adress', 'phone_number',
                    'age', 'gender', 'presence_absence_of_a_car',
                    'presence_absence_of_real_estate', 'month_income')

    list_filter = ('gender', 'presence_absence_of_a_car',
                   'presence_absence_of_real_estate', 'month_income')

    ordering = ('familia', 'name', 'otchestvo')

@admin.register(CreditStatement)
class CreditStatementAdmin(admin.ModelAdmin):
    search_fields = ('credit_code', 'client_code', 'loan_repayment_date', 'loan_issuance_date')
    list_display = ('loan_repayment_number', 'client_code',
                    'credit_code', 'credit_type_code', 'loan_issuance_date',
                    'loan_repayment_date', 'redemption_status')

    list_filter = ('redemption_status', 'credit_type_code')

    ordering = ('loan_repayment_number',)

