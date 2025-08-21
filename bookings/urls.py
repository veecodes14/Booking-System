from django.urls import path
from . import views

urlpatterns = [
    # Customer Profiles
    path("customers/", views.customer_profile_list, name="customer_profile_list"),

    # Service Providers
    path("service-providers/", views.service_provider_list, name="service_provider_list"),

    # Services
    path("services/", views.services_list, name="services_list"),

    # Availability Rules
    path("availability-rules/", views.availability_rule, name="availability_rule"),

    # Blackouts
    path("blackouts/", views.blackout, name="blackout"),

    # Bookings
    path("bookings/", views.booking_list, name="booking_list"),
    path("bookings/create/", views.create_booking_view, name="create_booking"),
    path("bookings/<int:id>/", views.booking_detail, name="booking_detail"),

    # Payments
    path("payments/", views.payment_list, name="payment_list"),

    # Reviews
    path("reviews/", views.review_list, name="review_list"),

    # Notifications
    path("notifications/", views.notification_list, name="notification_list"),

    # Calendar / Google OAuth
    path("calendar/credentials/", views.calendar_credential_list, name="calendar_credential_list"),
    path("calendar/event-links/", views.calendar_event_link_list, name="calendar_event_link_list"),
    path("calendar/init/", views.google_calendar_init, name="google_calendar_init"),
    path("calendar/redirect/", views.google_calendar_redirect, name="google_calendar_redirect"),
    path("calendar/create-event/", views.create_google_calendar_event, name="create_google_calendar_event"),

    # Google OAuth login / callback (if separate from calendar)
    path("oauth/login/", views.google_login, name="google_login"),
    path("oauth/callback/", views.google_callback, name="google_callback"),
]


