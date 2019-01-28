from django.urls import path, include

from apps.charity.restful.views import charity_join_view, charity_profile_view, charity_cash_project_create_view, \
    charity_cash_projects_view, non_charity_cash_project_create_view, non_charity_cash_projects_view, \
    charity_non_cash_project_add_time_slot_view, charity_non_cash_project_time_slots_view

cash_project_urlpatterns = [
    path('create/', charity_cash_project_create_view),
    path('', charity_cash_projects_view),
]

ncp_time_slots_urlpatterns = [
    path('create/', charity_non_cash_project_add_time_slot_view),
    path('', charity_non_cash_project_time_slots_view),
]

non_cash_project_urlpatterns = [
    path('create/', non_charity_cash_project_create_view),
    path('', non_charity_cash_projects_view),
    path('<project>/time-slots/', include(ncp_time_slots_urlpatterns))
]

urlpatterns = [
    path('join/', charity_join_view),
    path('', charity_profile_view),
    path('cash-projects/', include(cash_project_urlpatterns)),
    path('non-cash-projects/', include(non_cash_project_urlpatterns)),
]
