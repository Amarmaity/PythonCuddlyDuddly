from rest_framework import viewsets
from django.shortcuts import redirect, render
from .serializers import ProductSerializer
from .models import MasterProduct
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib import messages

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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(email=email)
                if user.user_type in ["admin", "super_admin"] and user.check_password(password):
                    request.session["admin_id"] = user.id
                    messages.success(request, f"Welcome Admin {user.name}!")
                    return redirect("admin_dashboard")
                else:
                    messages.error(request, "Invalid credentials or not an admin")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email")
    else:
        form = UserLoginForm()
    return render(request, "admin/auth/login.html", {"form": form})



def home_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    return render(request, "auth/home.html", {"user": user})