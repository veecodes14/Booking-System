from rest_framework import serializers
from .models import CustomerProfile, ServiceProvider, Service, AvailabilityRule, Blackout, Booking

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
        fields = ['id', 'provider', 'title', 'description', 'duration_minutes', 'price', 'category', 'buffer_before', 'buffer_after']

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


