from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/customer/", views.login_customer, name="login_customer"),
    path("login/provider/", views.login_provider, name="login_provider"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
]

