from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from bookings.models import CustomerProfile, ServiceProvider
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny


@api_view(['POST'])
@authentication_classes([])  # disables session auth (and CSRF)
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role')  # "customer" or "provider"

    if not role or role not in ['customer', 'provider']:
        return Response({'error': 'Role must be "customer" or "provider"'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username taken'}, status=400)

    # Create the user
    user = User.objects.create_user(username=username, password=password, email=email)

    # Create role-specific profile
    if role == 'customer':
        CustomerProfile.objects.create(user=user)
    else:
        ServiceProvider.objects.create(user=user, display_name=username)

    return Response({'message': f'{role.capitalize()} user created successfully'}, status=201)


@api_view(['POST'])
@authentication_classes([])  # disables session auth (and CSRF)
@permission_classes([AllowAny])
def login_customer(request):
    # same as above, but check role
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if user and hasattr(user, 'customerprofile'):
        login(request, user)
        return Response({"message": "Customer logged in"})
    return Response({"error": "Invalid credentials or not a customer"}, status=401)


@api_view(['POST'])
@authentication_classes([])  # disables session auth (and CSRF)
@permission_classes([AllowAny])
def login_provider(request):
    user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if user and hasattr(user, 'serviceprovider'):
        login(request, user)
        return Response({"message": "Service provider logged in"})
    return Response({"error": "Invalid credentials or not a service provider"}, status=401)

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('profile')
#         else:
#             messages.error(request, "Invalid username or password")
#             return redirect('login')
#     return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account as been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

        context = {
            'u_form' : u_form
    }

    return render (request, 'users/profile.html', context)

# Create your views here.
