# bookingsystem/services/availability.py

from datetime import datetime, timedelta, time
from django.utils.timezone import make_aware
from bookings import AvailabilityRule, Blackout, Booking

class AvailabilityService:

    @staticmethod
    def generate_slots(provider, service, start_date, end_date):
        """
        Generate available slots for a provider's service
        between start_date and end_date.
        """
        slots = []

        # Step 1: Start with provider's AvailabilityRules
        rules = AvailabilityRule.objects.filter(provider=provider, is_active=True)

        current_date = start_date
        while current_date <= end_date:
            weekday = current_date.strftime('%A')
            day_rules = rules.filter(day_of_week=weekday)

            for rule in day_rules:
                slots_for_day = AvailabilityService._slots_from_rule(
                    current_date, rule, service
                )
                slots.extend(slots_for_day)

            current_date += timedelta(days=1)

        # Step 2: Subtract blackouts
        slots = AvailabilityService._remove_blackouts(provider, slots)

        # Step 3: Subtract existing bookings (and buffers)
        slots = AvailabilityService._remove_conflicts(provider, service, slots)

        # Step 4 (Optional): Subtract Google busy events
        # To be added if Google sync is enabled

        return slots

    @staticmethod
    def _slots_from_rule(date, rule, service):
        """Generate slots from one availability rule."""
        slots = []
        start_dt = datetime.combine(date, rule.start_time)
        end_dt = datetime.combine(date, rule.end_time)
        duration = timedelta(minutes=service.duration_minutes)

        current = start_dt
        while current + duration <= end_dt:
            slots.append((make_aware(current), make_aware(current + duration)))
            current += duration
        return slots

    @staticmethod
    def _remove_blackouts(provider, slots):
        blackouts = Blackout.objects.filter(provider=provider)
        filtered = []
        for slot in slots:
            overlap = blackouts.filter(
                start_datetime__lt=slot[1],
                end_datetime__gt=slot[0]
            ).exists()
            if not overlap:
                filtered.append(slot)
        return filtered

    @staticmethod
    def _remove_conflicts(provider, service, slots):
        bookings = Booking.objects.filter(provider=provider)
        filtered = []
        for slot in slots:
            overlap = bookings.filter(
                start_time__lt=slot[1] + timedelta(minutes=service.buffer_after),
                end_time__gt=slot[0] - timedelta(minutes=service.buffer_before),
            ).exists()
            if not overlap:
                filtered.append(slot)
        return filtered
