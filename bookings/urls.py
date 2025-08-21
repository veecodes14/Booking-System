# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("oauth/login/", views.google_login, name="google_login"),
    path("oauth/callback/", views.google_callback, name="google_callback"),
    path("rest/v1/calendar/init/", views.google_calendar_init, name="google_init"),
    path("rest/v1/calendar/redirect/", views.google_calendar_redirect, name="google_redirect"),
    path("rest/v1/calendar/create/", views.create_google_calendar_event, name="google_create_event"),
]
