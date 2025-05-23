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

    def get_absolute_url(self):
        return reverse('bank:users_detail', args=[self.username])

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
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    surname = models.TextField()
    name = models.TextField()
    patronymic = models.TextField()
    adress = models.TextField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    age = models.IntegerField()
    sex = models.TextField(blank=True, null=True)
    flag_own_car = models.IntegerField(blank=True, null=True)
    flag_own_property = models.IntegerField(blank=True, null=True)
    month_income = models.IntegerField()
    count_children = models.IntegerField()
    education_type = models.TextField(blank=True, null=True)
    passport_serial_number = models.BigIntegerField(unique=True)

    def get_absolute_url(self):
        return reverse('bank:client_detail', args=[self.id])


    class Meta:
        managed = False
        db_table = 'clients'


class CreditStatement(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    number_of_the_loan_agreement = models.IntegerField(unique=True)
    credit_amount = models.IntegerField()
    term_month = models.IntegerField()
    monthly_payment = models.IntegerField()
    loan_opening_date = models.DateField(blank=True, null=True)
    repayment_status = models.IntegerField(blank=True, null=True)
    loan_type = models.ForeignKey('LoanTypes', models.DO_NOTHING, db_column='loan_type', blank=True, null=True)
    client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='client', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('bank:credit_statement_detail', args=[self.id])

    class Meta:
        managed = False
        db_table = 'credit_statement'


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


class LoanTypes(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    registration_number = models.IntegerField(unique=True)
    name_of_the_type = models.TextField()
    interest_rate = models.FloatField()

    def get_absolute_url(self):
        return reverse('bank:credit_type_detail', args=[self.id])

    class Meta:
        managed = False
        db_table = 'loan_types'


class Payroll(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    loan = models.ForeignKey(CreditStatement, models.DO_NOTHING, db_column='loan', blank=True, null=True)
    payment_date = models.DateField()
    payment_status = models.TextField()

    def get_absolute_url(self):
        return reverse('bank:payroll_detail', args=[self.id])

    class Meta:
        managed = False
        db_table = 'payroll'
