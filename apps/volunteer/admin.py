from django.contrib import admin

from apps.volunteer.models import Ability, Volunteer, VolunteerTimeSlot


class VolunteerTimeSlotAdmin(admin.ModelAdmin):
    search_fields = ['volunteer__user__username']
    list_display = ['volunteer', 'weekday', 'time', 'is_available', 'upcoming_project']
    list_filter = ['weekday', 'time']


admin.site.register(Ability)
admin.site.register(Volunteer)
admin.site.register(VolunteerTimeSlot, VolunteerTimeSlotAdmin)
