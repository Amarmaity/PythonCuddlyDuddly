from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm
from .models import User

# Create your views here.


def admin_dashboard(request):
     admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("custom_admin:login")
    admin_user = User.objects.get(id=admin_id)
    return render(request, "admin/adminDashboard.html", {"admin_user": admin_user})    