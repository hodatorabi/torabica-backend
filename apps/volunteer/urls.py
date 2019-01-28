from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from apps.volunteer.restful.views import abilities_view, volunteer_join_view, volunteer_profile_view, \
    volunteer_time_slot_update_view, volunteer_time_slots_view

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('profile/', volunteer_profile_view),
    path('join/', volunteer_join_view),
    path('time-slots/', volunteer_time_slots_view),
    path('time-slots/<id>/', volunteer_time_slot_update_view),
    path('abilities/', abilities_view)
]
