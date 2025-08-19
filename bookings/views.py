from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomerProfile, ServiceProvider, Service, AvailabilityRule, Blackout, Booking
from .serializers import CustomerProfileSerializer, ServiceProviderSerializer, ServiceSerializer, AvailabilityRuleSerialicer, BlackoutSerilizer, BookingSerializer
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
        
@api_view(['GET', 'POST'])
def services_list(request, format=None):

    if request.method == 'GET':
        services = Service.onjects.all()
        serializer = ServiceSerializer(services_list, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def services_list(request, format=None):

    if request.method == 'GET':
        services = Service.onjects.all()
        serializer = ServiceSerializer(services_list, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'POST'])
def availability_rule(request, format=None):

    if request.method == 'GET':
        availability_rule = AvailabilityRule.onjects.all()
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
        blackouts = Blackout.onjects.all()
        serializer = BlackoutSerilizer(blackouts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = BlackoutSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        







