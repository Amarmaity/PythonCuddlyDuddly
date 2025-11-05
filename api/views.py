from inspect import cleandoc
import json
import re
from webbrowser import get
from django.http import JsonResponse
from django.shortcuts import redirect, render
from phonenumbers import is_valid_number
from .serializers import ProductSerializer, SellerSerializer
from .models import MasterProduct, Seller
from .forms import UserRegistrationForm, UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.db.models import Q
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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


# def login_view(request):
#     if request.method == "POST":
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             phone = form.cleaned_data.get("phone")
#             password = form.cleaned_data.get("password")
#             try:
#                 user = User.objects.get(Q(email=email) | Q(phone=phone))
#                 if user.user_type in ["admin", "super_admin"] and user.check_password(password):
#                     request.session["admin_id"] = user.id
#                     messages.success(request, f"Welcome Admin {user.name}!")
#                     return redirect("custom_admin:adminDashboard")
#                 else:
#                     messages.error(request, "Invalid credentials or not an admin")
#             except User.DoesNotExist:
#                 messages.error(request, "No user found with this email or phone")
#     else:
#         form = UserLoginForm()
#     return render(request, "auth/login.html", {"form": form})



@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Detect if JSON request
        is_json = (
            request.headers.get("Content-Type", "").startswith("application/json")
            or request.headers.get("Accept", "").startswith("application/json")
        )

        if is_json:
            try:
                data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse({
                    "status": "error",
                    "errors": {"json": "Invalid JSON format"}
                }, status=400)
            email = data.get("email")
            phone = data.get("phone")
            password = data.get("password")
        else:
            form = UserLoginForm(request.POST)
            if not form.is_valid():
                messages.error(request, "Invalid form data")
                return render(request, "auth/login.html", {"form": form})
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")

        # Validate basic fields
        errors = {}
        if not email and not phone:
            errors["email"] = ["Email or phone is required"]
            errors["phone"] = ["Email or phone is required"]
        if not password:
            errors["password"] = ["Password is required"]

        if errors:
            if is_json:
                return JsonResponse({"status": "error", "errors": errors}, status=400)
            for msg_list in errors.values():
                for msg in msg_list:
                    messages.error(request, msg)
            return render(request, "auth/login.html", {"form": UserLoginForm()})

        # Authenticate user
        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
        except User.DoesNotExist:
            msg = "No account found with this email or phone"
            if is_json:
                return JsonResponse({
                    "status": "error",
                    "errors": {"email": msg, "phone": msg}
                }, status=404)
            messages.error(request, msg)
            return render(request, "auth/login.html", {"form": UserLoginForm()})

        if not user.check_password(password):
            msg = "Incorrect password"
            if is_json:
                return JsonResponse({"status": "error", "errors": {"password": msg}}, status=401)
            messages.error(request, msg)
            return render(request, "auth/login.html", {"form": UserLoginForm()})

        if user.user_type not in ["admin", "super_admin", "seller", "customer"]:
            msg = "You are not authorized to access the admin panel"
            if is_json:
                return JsonResponse({"status": "error", "errors": {"user_type": msg}}, status=403)
            messages.error(request, msg)
            return render(request, "auth/login.html", {"form": UserLoginForm()})

        # Start session
        request.session["admin_id"] = user.id
        if not request.session.session_key:
            request.session.create()

        # JSON response for API clients
        if is_json:
            return JsonResponse({
                "status": "success",
                "message": f"Welcome Admin {user.name}",
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": str(user.phone) if user.phone else None,
                    "user_type": user.user_type,
                    "session_token": request.session.session_key,
                },
            }, status=200)

        # Normal redirect for web
        messages.success(request, f"Welcome Admin {user.name}")
        return redirect("custom_admin:adminDashboard")

    # GET request — show login page
    form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})





def logout(request):
    request.session.flush()
    
    return redirect("api:login")


# Seller Api end point
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]



def home_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    return render(request, "auth/home.html", {"user": user})