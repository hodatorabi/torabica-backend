from django.urls import path, include

from apps.charity.restful.views import charity_join_view, charity_profile_view, charity_cash_project_create_view, \
    charity_cash_projects_view, charity_non_cash_project_create_view, charity_non_cash_projects_view, \
    charity_non_cash_project_add_time_slot_view, charity_non_cash_project_time_slots_view, \
    charity_non_cash_project_request_view, charity_requests_response_view, charity_incoming_requests_view, \
    charity_outgoing_requests_view, charity_feedback_view

cash_project_urlpatterns = [
    path('create/', charity_cash_project_create_view),
    path('', charity_cash_projects_view),
]

ncp_time_slots_urlpatterns = [
    path('create/', charity_non_cash_project_add_time_slot_view),
    path('', charity_non_cash_project_time_slots_view),
]

non_cash_project_urlpatterns = [
    path('create/', charity_non_cash_project_create_view),
    path('', charity_non_cash_projects_view),
    path('<project>/time-slots/', include(ncp_time_slots_urlpatterns)),
    path('<project>/request/<volunteer>/', charity_non_cash_project_request_view)
]

requests_urlpatterns = [
    path('incoming/', charity_incoming_requests_view),
    path('outgoing/', charity_outgoing_requests_view),
    path('<request_id>/', charity_requests_response_view)
]

urlpatterns = [
    path('join/', charity_join_view),
    path('', charity_profile_view),
    path('cash-projects/', include(cash_project_urlpatterns)),
    path('non-cash-projects/', include(non_cash_project_urlpatterns)),
    path('requests/', include(requests_urlpatterns)),
    path('send-feedback/<volunteer>/', charity_feedback_view)
]
