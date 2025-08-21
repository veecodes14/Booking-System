from django.db import models
from users.models import Users
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from timezone_field import TimeZoneField
from django.core.validators import MinValueValidator, MaxValueValidator



class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class ServiceProvider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    google_connection = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name if self.display_name else self.user.username
    

class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=50, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=1)  # Number of bookings allowed at the same time
    is_active = models.BooleanField(default=True)
    buffer_before = models.PositiveIntegerField(default=0) 
    buffer_after = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class AvailabilityRule(models.Model):

    DAY_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),   
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    day_of_week = models.CharField(choices=DAY_OF_WEEK, max_length=9)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.display_name} - {self.day_of_week} {self.start_time} to {self.end_time}"
    
class Blackout(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.provider.display_name} - {self.start_datetime} to {self.end_datetime}"
    
class Booking(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_datetime_utc = models.DateTimeField()
    end_datetime_utc = models.DateTimeField()
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)       # auto-updates on save

    def __str__(self):
        return f"Booking {self.id} - {self.customer.user.username} with {self.provider.display_name} on {self.start_datetime_utc}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD', choices=[
        ('GHS', 'Ghana Cedi'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),

    ])
    status = models.CharField(max_length=10, choices=[
        ('initiated', 'Initiated'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ])
    provider = models.CharField(max_length=15, choices=[
        ('paystack', 'Paystack'),
        ('momo', 'Momo'),
        ('t-cash', 'T-Cash'),
    ])
    transaction_ref = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.amount} {self.currency} via {self.provider}"

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=1
    )
    comment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Review for Booking {self.booking.id} - {self.rating} stars"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.CharField(max_length=15, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push')
    ])
    template_key = models.CharField(max_length=20)
    payload = models.JSONField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} via {self.channel}"
    
class CalendarCredential(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=20, choices=[
        ('google', 'Google'),
        ('outlook', 'Outlook'),
        ('apple', 'Apple')
    ])
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Calendar Credential for {self.user.username} - {self.provider}"
    def is_expired(self):
        return timezone.now() >= self.expires_at
    def refresh(self):
        # Logic to refresh the access token using the refresh token
        pass

class CalendarEventLink(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    calendar_credential = models.ForeignKey(CalendarCredential, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=255)
    event_url = models.URLField()

    def __str__(self):
        return f"Calendar Event Link for Booking {self.booking.id} - {self.event_id}"
    def create_event(self):
        # Logic to create a calendar event using the calendar credential
        pass
    


