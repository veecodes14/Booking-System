from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomerProfile, ServiceProvider, Service, AvailabilityRule, Blackout, Booking, Payment, Review, Notification, CalendarCredential, CalendarEventLink
from .serializers import CustomerProfileSerializer, ServiceProviderSerializer, ServiceSerializer, AvailabilityRuleSerialicer, BlackoutSerilizer, BookingSerializer, PaymentSerializer, ReviewSerializer, NotificationSerializer, CalendarCredentialSerializer, CalendarEventLinkSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django.contrib import messages
from django.conf import settings

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

        
        
        







