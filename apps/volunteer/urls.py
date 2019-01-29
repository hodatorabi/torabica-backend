from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token

from apps.volunteer.restful.views import abilities_view, volunteer_join_view, volunteer_profile_view, \
    volunteer_time_slot_update_view, volunteer_time_slots_view, cash_project_create_transaction, \
    volunteer_cash_projects_view, \
    volunteer_incoming_requests_view, volunteer_outgoing_requests_view, volunteer_requests_response_view, \
    volunteer_non_cash_project_request_view, volunteer_non_cash_projects_view, volunteer_feedback_view, \
    volunteer_feedbacks_view, cash_projects_view

requests_urlpatterns = [
    path('incoming/', volunteer_incoming_requests_view),
    path('outgoing/', volunteer_outgoing_requests_view),
    path('<request_id>/', volunteer_requests_response_view)
]

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('profile/', volunteer_profile_view),
    path('join/', volunteer_join_view),
    path('time-slots/', volunteer_time_slots_view),
    path('time-slots/<id>/', volunteer_time_slot_update_view),
    path('abilities/', abilities_view),
    path('pay/<project>/', cash_project_create_transaction),
    path('my-cash-projects/', volunteer_cash_projects_view),
    path('my-non-cash-projects/', volunteer_non_cash_projects_view),
    path('request/<charity>/<project>/', volunteer_non_cash_project_request_view),
    path('requests/', include(requests_urlpatterns)),
    path('give-feedback/<charity>', volunteer_feedback_view),
    path('my-feedbacks/', volunteer_feedbacks_view),
    path('cash-projects/', cash_projects_view)
]
