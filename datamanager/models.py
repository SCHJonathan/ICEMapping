# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid
from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class Geo(models.Model):
    geoid = models.BigIntegerField(db_column='GEOID', blank=False, null=False, primary_key=True)  # Field name made lowercase.
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geo'


class Tidychampaign(models.Model):
    geoid = models.BigIntegerField(db_column='GEOID', blank=False, null=False, primary_key=True)  # Field name made lowercase.
    block = models.TextField(db_column='Block', blank=True, null=True)  # Field name made lowercase.
    geography = models.TextField(db_column='Geography', blank=True, null=True)  # Field name made lowercase.
    population = models.IntegerField(db_column='Population', blank=True, null=True)  # Field name made lowercase.
    white = models.IntegerField(db_column='White', blank=True, null=True)  # Field name made lowercase.
    black = models.IntegerField(db_column='Black', blank=True, null=True)  # Field name made lowercase.
    asian = models.IntegerField(db_column='Asian', blank=True, null=True)  # Field name made lowercase.
    otherrace = models.IntegerField(db_column='OtherRace', blank=True, null=True)  # Field name made lowercase.
    male = models.IntegerField(db_column='Male', blank=True, null=True)  # Field name made lowercase.
    female = models.IntegerField(db_column='Female', blank=True, null=True)  # Field name made lowercase.
    young = models.IntegerField(db_column='Young', blank=True, null=True)  # Field name made lowercase.
    middle = models.IntegerField(db_column='Middle', blank=True, null=True)  # Field name made lowercase.
    old = models.IntegerField(db_column='Old', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tidychampaign'

class CommentDB(models.Model):
    username = models.TextField(db_column='Username', blank=False, null=False)  # Field name made lowercase.
    geoid = models.CharField(max_length=20, db_column='GEOID', blank=False, null=False)  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'commentdb'


class Socio(models.Model):
    geography = models.TextField(db_column='Geography', blank=True, null=True)  # Field name made lowercase.
    year_built = models.IntegerField(blank=True, null=True)
    median_income = models.IntegerField(db_column='Median_Income', blank=True, null=True)  # Field name made lowercase.
    median_rent = models.IntegerField(db_column='Median_rent', blank=True, null=True)  # Field name made lowercase.
    estimate_total_field = models.IntegerField(db_column='Estimate..Total.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    no_schooling = models.IntegerField(db_column='No_schooling', blank=True, null=True)  # Field name made lowercase.
    nursery_school = models.IntegerField(db_column='Nursery_school', blank=True, null=True)  # Field name made lowercase.
    kindergarten = models.IntegerField(db_column='Kindergarten', blank=True, null=True)  # Field name made lowercase.
    x1st_grade = models.IntegerField(db_column='X1st_grade', blank=True, null=True)  # Field name made lowercase.
    x2nd_grade = models.IntegerField(db_column='X2nd.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x3rd_grade = models.IntegerField(db_column='X3rd.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x4th_grade = models.IntegerField(db_column='X4th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x5th_grade = models.IntegerField(db_column='X5th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x6th_grade = models.IntegerField(db_column='X6th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x7th_grade = models.IntegerField(db_column='X7th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x8th_grade = models.IntegerField(db_column='X8th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x9th_grade = models.IntegerField(db_column='X9th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x10th_grade = models.IntegerField(db_column='X10th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x11th_grade = models.IntegerField(db_column='X11th.grade', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    x12th_grade_no_diploma = models.IntegerField(db_column='X12th.grade..no.diploma', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    regular_high_school_diploma = models.IntegerField(db_column='Regular.high.school.diploma', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ged_or_alternative_credential = models.IntegerField(db_column='GED.or.alternative.credential', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    some_college_less_than_1_year = models.IntegerField(db_column='Some.college..less.than.1.year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    some_college_1_or_more_years_no_degree = models.IntegerField(db_column='Some.college..1.or.more.years..no.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    associate_s_degree = models.IntegerField(db_column='Associate.s.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bachelor_s_degree = models.IntegerField(db_column='Bachelor.s.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    master_s_degree = models.IntegerField(db_column='Master.s.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    professional_school_degree = models.IntegerField(db_column='Professional.school.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    doctorate_degree = models.IntegerField(db_column='Doctorate.degree', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'socio'

class Rate(models.Model):
    username = models.TextField(db_column='Username', null=False, primary_key=True)
    race = models.TextField(db_column='Race', blank=True, null=True)  # Field name made lowercase.
    gender = models.TextField(db_column='Gender', blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    dept = models.TextField(db_column='Dept', blank=True, null=True)  # Field name made lowercase.
    block = models.TextField(db_column='Block', blank=True, null=True)  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rate'

class Userinfo(models.Model):
    username = models.CharField(db_column='Username', max_length=30, blank=True, null=True)  # Field name made lowercase.
    race = models.TextField(db_column='Race', blank=True, null=True)  # Field name made lowercase.
    gender = models.TextField(db_column='Gender', blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    dept = models.TextField(db_column='Dept', blank=True, null=True)  # Field name made lowercase.
    block = models.TextField(db_column='Block', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userinfo'
