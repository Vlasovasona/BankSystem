# модели данных приложения.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clients(models.Model):
    client_code = models.IntegerField(db_column='Client_code', primary_key=True)  # Field name made lowercase.
    familia = models.TextField(db_column='Familia', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    otchestvo = models.TextField(db_column='Otchestvo', blank=True, null=True)  # Field name made lowercase.
    adress = models.TextField(db_column='Adress', blank=True, null=True)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_number', max_length=15, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    gender = models.TextField(db_column='Gender', blank=True, null=True)  # Field name made lowercase.
    presence_absence_of_a_car = models.IntegerField(db_column='Presence_absence_of_a_car', blank=True, null=True)  # Field name made lowercase.
    presence_absence_of_real_estate = models.IntegerField(db_column='Presence_absence_of_real_estate', blank=True, null=True)  # Field name made lowercase.
    month_income = models.IntegerField(db_column='Month_income', blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('bank:client_detail', args=[self.client_code])

    class Meta:
        managed = False
        db_table = 'clients'
        ordering = ['familia', 'name', 'otchestvo']


class CreditStatement(models.Model):
    loan_repayment_number = models.IntegerField(db_column='Loan_repayment_number', primary_key=True)  # Field name made lowercase.
    loan_issuance_date = models.DateField(db_column='Loan_issuance_date', blank=True, null=True)  # Field name made lowercase.
    loan_repayment_date = models.DateField(db_column='Loan_Repayment_Date', blank=True, null=True)  # Field name made lowercase.
    redemption_status = models.IntegerField(db_column='Redemption_status', blank=True, null=True)  # Field name made lowercase.
    credit_code = models.ForeignKey('Credits', models.DO_NOTHING, db_column='Credit_code', blank=True, null=True)  # Field name made lowercase.
    credit_type_code = models.ForeignKey('CreditType', models.DO_NOTHING, db_column='Credit_type_code', blank=True, null=True)  # Field name made lowercase.
    client_code = models.ForeignKey(Clients, models.DO_NOTHING, db_column='Client_code', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'credit_statement'


class CreditType(models.Model):
    credit_type_code = models.IntegerField(db_column='Credit_type_code', primary_key=True)  # Field name made lowercase.
    credit_type_name = models.TextField(db_column='Credit_type_name', blank=True, null=True)  # Field name made lowercase.
    credit_percent = models.DecimalField(db_column='Credit_percent', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('bank:credit_type_detail', args=[self.credit_type_code])

    class Meta:
        managed = False
        db_table = 'credit_type'


class Credits(models.Model):
    credit_code = models.IntegerField(db_column='Credit_code', primary_key=True)
    credit_amount = models.DecimalField(db_column='Credit_amount', max_digits=20, decimal_places=2, blank=True, null=True)
    term_month = models.IntegerField(db_column='Term_month', blank=True, null=True)
    monthly_payment_amount = models.DecimalField(db_column='Monthly_payment_amount', max_digits=10, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('bank:credit_detail', args=[self.credit_code])

    class Meta:
        managed = False
        db_table = 'credits'




class DepositTypes(models.Model):
    deposit_type_code = models.IntegerField(db_column='Deposit_type_code', primary_key=True)  # Field name made lowercase.
    name_of_deposit_type = models.TextField(db_column='Name_of_deposit_type', blank=True, null=True)  # Field name made lowercase.
    deposit_percent = models.DecimalField(db_column='Deposit_percent', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('bank:deposit_type_detail', args=[self.deposit_type_code])

    class Meta:
        managed = False
        db_table = 'deposit_types'


class Deposits(models.Model):
    deposit_code = models.IntegerField(db_column='Deposit_code', primary_key=True)  # Field name made lowercase.
    deposit_amount = models.DecimalField(db_column='Deposit_amount', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('bank:deposit_detail', args=[self.deposit_code])

    class Meta:
        managed = False
        db_table = 'deposits'


class DescriptiveStatistics(models.Model):
    calculation_date = models.DateField(db_column='Calculation_date', blank=True, null=True)  # Field name made lowercase.
    average_value = models.DecimalField(db_column='Average_value', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    total_sum = models.DecimalField(db_column='Total_sum', max_digits=20, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    maximum_value = models.DecimalField(db_column='Maximum_value', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    minimum_value = models.DecimalField(db_column='Minimum_value', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'descriptive_statistics'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class StatementOfDeposits(models.Model):
    deposit_closing_number = models.IntegerField(db_column='Deposit_closing_number', primary_key=True)  # Field name made lowercase.
    deposit_opening_date = models.DateField(db_column='Deposit_opening_date', blank=True, null=True)  # Field name made lowercase.
    deposit_ending_date = models.DateField(db_column='Deposit_ending_date', blank=True, null=True)  # Field name made lowercase.
    deposit_closing_status = models.IntegerField(db_column='Deposit_Closing_Status', blank=True, null=True)  # Field name made lowercase.
    client_code = models.ForeignKey(Clients, models.DO_NOTHING, db_column='Client_code', blank=True, null=True)  # Field name made lowercase.
    deposit_code = models.ForeignKey(Deposits, models.DO_NOTHING, db_column='Deposit_code', blank=True, null=True)  # Field name made lowercase.
    deposit_type_code = models.ForeignKey(DepositTypes, models.DO_NOTHING, db_column='Deposit_type_code', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'statement_of_deposits'


class Statistics(models.Model):
    open_deposits = models.IntegerField(blank=True, null=True)
    closed_deposits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics'

