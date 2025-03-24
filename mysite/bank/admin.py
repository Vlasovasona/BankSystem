# Регистрация моделей для добавления их в систему администрирования Django
from django.contrib import admin
from .models import AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser
from .models import AuthUserGroups, AuthUserUserPermissions
from .models import Clients, CreditStatement, LoanTypes, Payroll
from .models import DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession



admin.site.register(AuthGroup)
admin.site.register(AuthGroupPermissions)
admin.site.register(AuthPermission)
admin.site.register(AuthUser)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(Clients)
admin.site.register(CreditStatement)
admin.site.register(LoanTypes)
admin.site.register(Payroll)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)



@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    search_fields = ('surname', 'name', 'patronymic', 'passport_serial_number')
    list_display = ('surname', 'name', 'patronymic', 'adress', 'phone_number',
                    'age', 'sex', 'flag_own_car',
                    'flag_own_property', 'month_income', 'count_children',
                    'education_type', 'passport_serial_number'
                    )

    list_filter = ('gender', 'flag_own_car',
                   'flag_own_property', 'month_income')

    ordering = ('surname', 'name', 'patronymic')


@admin.register(CreditStatement)
class CreditStatementAdmin(admin.ModelAdmin):
    search_fields = ('number_of_the_loan_agreement', 'loan_opening_date', 'loan_type')
    list_display = ('number_of_the_loan_agreement', 'credit_amount',
                    'term_month', 'monthly_payment', 'loan_opening_date',
                    'repayment_status', 'loan_type', 'client')

    list_filter = ('redemption_status', 'credit_type_code')


@admin.register(LoanTypes)
class CreditTypeAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name_of_the_type', 'interest_rate')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('loan', 'payment_date', 'payment_status')