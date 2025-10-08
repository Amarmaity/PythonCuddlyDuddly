from urllib import request
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from api.forms import UserLoginForm
from api.models import User

# Create your views here.


def admin_dashboard(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("api:login")
    admin_user = User.objects.get(id=admin_id)
    return render(request, "custom_admin/adminDashboard.html", {"admin_user": admin_user})


@login_required
def saller_index(request):
    
    return render(request, "custom_admin/sallers/index.html")


@login_required
def saller_application(request):

    return render(request, "custom_admin/sallers/saller_application.html")


@login_required
def kyc_compliance(request):

    return render(request, "custom_admin/sallers/kyc_complince.html")


@login_required
def payout(request):

    return render(request, "custom_admin/sallers/payout.html")


@login_required
def product_index(request):

    return render(request, "custom_admin/products/product_index.html")


@login_required
def category_index(request):
    
    return render(request, "custom_admin/products/category_index.html")



@login_required
def customer_index(request):

    return render(request, "custom_admin/customers/customer_index.html")


@login_required
def review_index(request):

    return render(request, "custom_admin/customers/review_index.html")


@login_required
def report_sales(request):

    return render(request, "custom_admin/reports/reports_sales.html")


@login_required
def report_revenue(request):

    return render(request, "custom_admin/reports/reports_revenue.html")


@login_required
def reports_saller(request):

    return render(request, "custom_admin/reports/reports_saller.html")


@login_required
def report_customer(request):

    return render(request, "custom_admin/reports/report_customer.html")



@login_required
def setting_index(request):

    return render(request, "custom_admin/setting/setting_index.html")



@login_required
def setting_payment(request):

    return render(request, "custom_admin/setting/setting_payment.html")



@login_required
def setting_shipping(request):

    return render(request, "custom_admin/setting/settings_shipping.html")


@login_required
def roles_indexinig(request):

    return render(request, "custom_admin/setting/roles_indexing.html")