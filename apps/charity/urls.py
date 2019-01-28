from django.urls import path

from apps.charity.restful.views import charity_join_view, charity_profile_view, charity_cash_project_create_view, \
    charity_cash_projects_view

urlpatterns = [
    path('join/', charity_join_view),
    path('', charity_profile_view),
    path('create-cash-project/', charity_cash_project_create_view),
    path('cash-projects/', charity_cash_projects_view)
]
