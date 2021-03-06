from django.contrib import admin

from apps.charity.models import CashProject, CashProjectTransaction, Charity, NonCashProject, NonCashProjectTimeSlot, \
    NonCashProjectRequest, Feedback


class CharityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user__username', 'phone_number']
    list_display = ['name', 'username', 'phone_number']


class CashProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'funded_amount', 'target_amount', 'start_date', 'end_date']


class CashProjectTransactionAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'project', 'amount']


class NonCashProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']


class NonCashProjectNonCashProjectTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['project', 'weekday', 'time']
    list_filter = ['weekday', 'time']


class NonCashProjectRequestAdmin(admin.ModelAdmin):
    list_display = ['project', 'volunteer', 'charity', 'target', 'status']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['charity', 'volunteer', 'target', 'comment', 'rating']


admin.site.register(Charity, CharityAdmin)
admin.site.register(CashProject, CashProjectAdmin)
admin.site.register(CashProjectTransaction, CashProjectTransactionAdmin)
admin.site.register(NonCashProject, NonCashProjectAdmin)
admin.site.register(NonCashProjectTimeSlot, NonCashProjectNonCashProjectTimeSlotAdmin)
admin.site.register(NonCashProjectRequest, NonCashProjectRequestAdmin)
admin.site.register(Feedback, FeedbackAdmin)
