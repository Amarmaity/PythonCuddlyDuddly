from cmath import phase
from xml.etree.ElementTree import QName
from django.shortcuts import redirect, render
from .serializers import ProductSerializer
from .models import MasterProduct
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.db.models import Q
from django.contrib import messages
from rest_framework import viewsets

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = MasterProduct.objects.all()
    serializer_class = ProductSerializer


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(Q(email=email) | Q(phone=phone))
                if user.user_type in ["admin", "super_admin"] and user.check_password(password):
                    request.session["admin_id"] = user.id
                    messages.success(request, f"Welcome Admin {user.name}!")
                    return redirect("custom_admin:adminDashboard")
                else:
                    messages.error(request, "Invalid credentials or not an admin")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email or phone")
    else:
        form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})


def logout(request):
    request.session.flush()
    
    return redirect("api:login")


def home_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    return render(request, "auth/home.html", {"user": user})