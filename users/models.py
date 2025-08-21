from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField

class Users(models.Model):
    USER_ROLE = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    timezone = TimeZoneField(default='UTC')
    role = models.CharField(max_length=10, choices=USER_ROLE, default='customer')
    google_access_token = models.TextField(null=True, blank=True)
    google_refresh_token = models.TextField(null=True, blank=True)
    google_token_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    

