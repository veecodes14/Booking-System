# bookings/services.py

from django.db.models import Q
from django.utils import timezone
from bookings.models import Booking, Service, Blackout, AvailabilityRule


def create_booking(customer, service, start_datetime):
    end_datetime = start_datetime + timezone.timedelta(minutes=service.duration_minutes)

    # Buffer times
    buffered_start = start_datetime - timezone.timedelta(minutes=service.buffer_before)
    buffered_end = end_datetime + timezone.timedelta(minutes=service.buffer_after)

    # Availability check
    weekday = start_datetime.strftime("%A")
    available = AvailabilityRule.objects.filter(
        provider=service.provider,
        day_of_week=weekday,
        is_active=True,
        start_time__lte=start_datetime.time(),
        end_time__gte=end_datetime.time()
    ).exists()
    if not available:
        raise ValueError("Provider is not available at this time.")

    # Blackout check
    if Blackout.objects.filter(
        provider=service.provider,
        start_datetime__lt=buffered_end,
        end_datetime__gt=buffered_start
    ).exists():
        raise ValueError("This slot is blocked.")

    # Overlap check
    overlapping = Booking.objects.filter(
        provider=service.provider,
        status="confirmed",
        start_datetime_utc__lt=buffered_end,
        end_datetime_utc__gt=buffered_start
    ).exists()
    if overlapping:
        raise ValueError("This slot is already booked.")

    # Create booking
    booking = Booking.objects.create(
        customer=customer,
        provider=service.provider,
        service=service,
        start_datetime_utc=start_datetime,
        end_datetime_utc=end_datetime,
        price_snapshot=service.price,  # locks price at booking time
        status="pending"  # you might confirm after payment
    )

    return booking
