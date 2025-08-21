from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomerProfile, ServiceProvider, Service, AvailabilityRule, Blackout, Booking, Payment, Review, Notification, CalendarCredential, CalendarEventLink
from .serializers import CustomerProfileSerializer, ServiceProviderSerializer, ServiceSerializer, AvailabilityRuleSerialicer, BlackoutSerilizer, BookingSerializer, PaymentSerializer, ReviewSerializer, NotificationSerializer, CalendarCredentialSerializer, CalendarEventLinkSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Request, Response
from rest_framework import status, generics, filters
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json
import os

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")
SCOPES = ["https://www.googleapis.com/auth/calendar"]


@api_view(['GET', 'POST'])
def customer_profile_list(request, format=None):

    if request.method == 'GET':
        customers = CustomerProfile.objects.all()
        serializer = CustomerProfileSerializer(customers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CustomerProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def service_provider_list(request, format=None):

    if request.method == 'GET':
        service_providers = ServiceProvider.objects.all()
        serializer = ServiceProviderSerializer(service_providers, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ServiceProviderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ServiceProviderListAPIView:
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category', 'price range', 'location', 'avg_rating', 'availability']
    ordering_fields = ['category', 'location']
        
@api_view(['GET', 'POST'])
def services_list(request, format=None):

    if request.method == 'GET':
        services = Service.onjects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class ServiceListAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'duration_minutes', 'price', 'category']
    ordering_fields = ['price', 'category']
        
@api_view(['GET', 'POST'])
def availability_rule(request, format=None):

    if request.method == 'GET':
        availability_rule = AvailabilityRule.objects.all()
        serializer = AvailabilityRuleSerialicer(availability_rule, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = AvailabilityRuleSerialicer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def blackout(request, format=None):

    if request.method == 'GET':
        blackouts = Blackout.objects.all()
        serializer = BlackoutSerilizer(blackouts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BlackoutSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def booking_list(request, format=None):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def payment_list(request, format=None):
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
def review_list(request, format=None):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def notification_list(request, format=None):
    if request.method == 'GET':
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def calendar_credential_list(request, format=None):
    if request.method == 'GET':
        credentials = CalendarCredential.objects.all()
        serializer = CalendarCredentialSerializer(credentials, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CalendarCredentialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def calendar_event_link_list(request, format=None):
    if request.method == 'GET':
        event_links = CalendarEventLink.objects.all()
        serializer = CalendarEventLinkSerializer(event_links, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CalendarEventLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# Step 1: Redirect user to Google Login
def google_login(request):
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/oauth/callback/"
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

# Step 2: Google sends user back here
def google_callback(request):
    code = request.GET.get("code")
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:8000/oauth/callback/"
    )
    flow.fetch_token(code=code)

    credentials = flow.credentials

    data = {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return JsonResponse(data)

@login_required
def google_calendar_init(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri="http://127.0.0.1:8000/rest/v1/calendar/redirect/"
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@login_required
def google_calendar_redirect(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=settings.GOOGLE_SCOPES,
        redirect_uri="http://127.0.0.1:8000/rest/v1/calendar/redirect/"
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
        
        
        # Save tokens in DB/session if needed
    request.session['google_token'] = credentials.to_json()

    return redirect("/")  # send back to homepage (or dashboard)

@login_required
def create_google_calendar_event(request):
    creds = Credentials.from_authorized_user_info(json.loads(request.session['google_token']))
    service = build("calendar", "v3", credentials=creds)

    event = {
        'summary': 'Booking with Service Provider',
        'location': 'Online',
        'description': 'Your booking was confirmed.',
        'start': {
            'dateTime': '2025-08-21T09:00:00-07:00',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': '2025-08-21T10:00:00-07:00',
            'timeZone': 'UTC',
        },
    }

    service.events().insert(calendarId='primary', body=event).execute()
    return redirect("/")

def get_calendar_service(customer_profile):

    # profile = customer_profile.profile

    if not customer_profile.google_access_token:
        return None  # user hasn't linked Google yet

    creds = Credentials(
        token=customer_profile.google_access_token,
        refresh_token=customer_profile.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com",
        client_secret="YOUR_GOOGLE_CLIENT_SECRET",
        expiry=customer_profile.google_token_expiry,
    )

    # auto-refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # update DB
        customer_profile.google_access_token = creds.token
        customer_profile.google_token_expiry = creds.expiry
        customer_profile.save()

    return build("calendar", "v3", credentials=creds)







