import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.utils import timezone


def get_calendar_service(customer):
    """
    Returns an authorized Google Calendar service instance
    for the given customer.
    """
    if not customer.google_access_token or not customer.google_refresh_token:
        return None  # customer hasn't linked Google yet

    creds = Credentials(
        token=customer.google_access_token,
        refresh_token=customer.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="YOUR_GOOGLE_CLIENT_ID",
        client_secret="YOUR_GOOGLE_CLIENT_SECRET",
        scopes=["https://www.googleapis.com/auth/calendar"],
    )

    # Refresh token if expired
    if creds.expired and creds.refresh_token:
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
        # TODO: save the new access token back to customer model

    service = build("calendar", "v3", credentials=creds)
    return service

def create_calendar_event(customer, booking):
    """
    Pushes a booking to the customer's Google Calendar.
    """
    service = get_calendar_service(customer)
    if not service:
        return None  # Customer hasn’t linked Google

    event_body = {
        "summary": booking.service.name,
        "description": f"Booking with {booking.provider.name} for {booking.service.name}.",
        "start": {
            "dateTime": booking.start_datetime_utc.isoformat(),
            "timeZone": "UTC",  # replace with provider/customer tz if needed
        },
        "end": {
            "dateTime": booking.end_datetime_utc.isoformat(),
            "timeZone": "UTC",
        },
        "attendees": [
            {"email": customer.email},
            {"email": booking.provider.email},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},  # 1 day before
                {"method": "popup", "minutes": 10},       # 10 min before
            ],
        },
    }

    event = (
        service.events()
        .insert(calendarId="primary", body=event_body)
        .execute()
    )

    return event
