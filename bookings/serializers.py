from rest_framework import serializers
from .models import CustomerProfile, ServiceProvider, Service, AvailabilityRule, Blackout, Booking, Payment, Review, Notification, CalendarCredential, CalendarEventLink

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields=  ['id', 'user', 'created_at', 'updated_at', 'default_location', 'notes']

class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ['id', 'user', 'display_name', 'bio', 'business_name', 'address', 'avg_rating', 'google_connection']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'provider', 'title', 'description', 'duration_minutes', 'price', 'category', 'capacity', 'is_active', 'buffer_before', 'buffer_after']
 

class AvailabilityRuleSerialicer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityRule
        fields = ['id', 'provider', 'day_of_week', 'start_time', 'end_time', 'is_active']

class BlackoutSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Blackout
        fields = ['id', 'provider', 'start_datetime', 'end_datetime', 'reason']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer', 'provider', 'service', 'start_datetime_utc', 'end_datetime_utc', 'price_snapshot', 'status', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        start_datetime_utc = cleaned_data.get('start_datetime_utc')
        end_datetime_utc = cleaned_data.get('end_time')
        if service and start_datetime_utc and end_datetime_utc:
            if start_datetime_utc>= end_datetime_utc:
                raise serializers.ValidationError("Start time must be before end time.")
            if not service.is_available(start_datetime_utc, end_datetime_utc):
                raise serializers.ValidationError("Item is not available during the selected time.")
    
        if service and start_datetime_utc and end_datetime_utc:
            # Check for overlapping bookings for the same item
            overlapping_bookings = Booking.objects.filter(
                service=service,
                start_time__lt=end_datetime_utc,
                end_time__gt=start_datetime_utc
            ).exclude(id=self.instance.id if self.instance else None
            ).count()

            if overlapping_bookings >= service.capacity:
                raise serializers.ValidationError("This item is not available during the selected time.")

        return cleaned_data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'currency', 'provider', 'transaction_ref']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'rating', 'comment']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']

class CalendarCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarCredential
        fields = ['id', 'user', 'credential_data']

class CalendarEventLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEventLink
        fields = ['id', 'booking', 'event_link', 'created_at']




