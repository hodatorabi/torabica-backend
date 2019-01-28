from django.urls import path

from apps.charity.restful.views import charity_join_view, charity_profile_view

urlpatterns = [
    path('join/', charity_join_view),
    path('', charity_profile_view)
]
