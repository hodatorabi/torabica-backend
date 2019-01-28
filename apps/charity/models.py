from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from apps.volunteer.constants import SLOT_TIME_CHOICES, WEEKDAY_CHOICES, REQUEST_STATUS_CHOICES, REQUEST_TARGET_CHOICES


class Charity(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, related_name='charity')

    name = models.CharField(max_length=50, db_index=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'charities'

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.name


class BaseProject(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CashProject(BaseProject):
    charity = models.ForeignKey('Charity', on_delete=models.PROTECT, related_name='cash_projects')
    target_amount = models.PositiveIntegerField()
    volunteers = models.ManyToManyField('volunteer.Volunteer', related_name='cash_projects',
                                        through='CashProjectTransaction', blank=True)

    @property
    def funded_amount(self):
        return self.transactions.aggregate(sum_amount=Coalesce(Sum('amount'), 0))['sum_amount']


class CashProjectTransaction(models.Model):
    project = models.ForeignKey('CashProject', on_delete=models.PROTECT, related_name='transactions')
    volunteer = models.ForeignKey('volunteer.Volunteer', on_delete=models.PROTECT, related_name='transactions')
    amount = models.PositiveIntegerField()


class NonCashProject(BaseProject):
    charity = models.ForeignKey('Charity', on_delete=models.PROTECT, related_name='non_cash_projects')

    need_male = models.BooleanField(db_index=True)
    need_female = models.BooleanField(db_index=True)
    min_age = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    max_age = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    city = models.CharField(max_length=40, db_index=True, null=True, blank=True)

    abilities = models.ManyToManyField('volunteer.Ability', related_name='projects', blank=True)
    volunteers = models.ManyToManyField('volunteer.Volunteer', related_name='non_cash_projects', blank=True)


class NonCashProjectTimeSlot(models.Model):
    project = models.ForeignKey('NonCashProject', on_delete=models.PROTECT, related_name='time_slots')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, db_index=True)
    time = models.IntegerField(choices=SLOT_TIME_CHOICES, db_index=True)

    class Meta:
        unique_together = ('project', 'weekday', 'time')


class NonCashProjectRequest(models.Model):
    project = models.ForeignKey('NonCashProject', on_delete=models.PROTECT, related_name='requests')
    volunteer = models.ForeignKey('volunteer.Volunteer', on_delete=models.PROTECT, related_name='requests')
    charity = models.ForeignKey('Charity', on_delete=models.PROTECT, related_name='requests')

    target = models.IntegerField(choices=REQUEST_TARGET_CHOICES)
    message = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=REQUEST_STATUS_CHOICES, db_index=True, default=0)

    class Meta:
        unique_together = ('project', 'volunteer', 'charity')
