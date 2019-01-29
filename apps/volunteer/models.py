from datetime import timedelta

from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.volunteer.constants import GENDER_CHOICES, SLOT_TIME_CHOICES, WEEKDAY_CHOICES


class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'abilities'

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT, related_name='volunteer')

    name = models.CharField(max_length=50, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True, null=True, blank=True)
    age = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    abilities = models.ManyToManyField('Ability', related_name='users', blank=True)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=40, db_index=True, null=True, blank=True)

    @property
    def username(self):
        return self.user.username

    @property
    def avg_rating(self):
        return self.feedbacks.filter(target=1).aggregate(avg_amount=Coalesce(Avg('rating'), 0))['avg_amount']

    def create_initial_data(self):
        time_slots = []
        for weekday, day_name in WEEKDAY_CHOICES:
            for time, time_name in SLOT_TIME_CHOICES:
                time_slots.append(VolunteerTimeSlot(volunteer=self, weekday=weekday, time=time))
        VolunteerTimeSlot.objects.bulk_create(time_slots)

    def __str__(self):
        return self.username


@receiver(post_save, sender=Volunteer)
def volunteer_post_save(instance: Volunteer, created: bool, **kwargs):
    if created:
        instance.create_initial_data()


class VolunteerTimeSlot(models.Model):
    volunteer = models.ForeignKey('Volunteer', on_delete=models.PROTECT, related_name='time_slots')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, db_index=True)
    time = models.IntegerField(choices=SLOT_TIME_CHOICES, db_index=True)

    is_available = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = ('volunteer', 'weekday', 'time')

    @property
    def upcoming_project(self):
        if not self.is_available:
            return None
        today = timezone.now().date()
        diff_day = self.weekday - today.weekday()
        if diff_day < 0:
            diff_day += 7
        target_day = today + timedelta(days=diff_day)
        return self.volunteer.non_cash_projects \
            .filter(start_date__lte=target_day, end_date__gte=target_day) \
            .filter(time_slots__weekday=self.weekday, time_slots__time=self.time) \
            .first()
