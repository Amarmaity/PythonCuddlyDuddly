from urllib import request
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from api.forms import UserLoginForm
from api.models import Seller, User
from django.core.paginator import Paginator
from .decorators import admin_login_required
from custom_admin.forms import SellerForm
# Create your views here.

def admin_dashboard(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("api:login")
    admin_user = User.objects.get(id=admin_id)
    return render(request, "custom_admin/adminDashboard.html", {"admin_user": admin_user})



@admin_login_required
def saller_index(request):
    seller_list = Seller.objects.all()

    # Search
    search = request.GET.get('search')
    if search:
        sellers = sellers.filter(
            Q(name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Status
    status = request.GET.get('status')
    if status == '1':
        sellers = sellers.filter(is_active=True)
    elif status == '0':
        sellers = sellers.filter(is_active=False)
    
    # Sort
    sort = request.GET.get('sort')
    if sort == 'latest':
        sellers = sellers.order_by('-created_at')
    elif sort == 'oldest':
        sellers = sellers.order_by('created_at')
    elif sort == 'name':
        sellers = sellers.order_by('name')
    

    paginator = Paginator(seller_list, 10)
    page_number = request.GET.get('page')
    sellers = paginator.get_page(page_number)
    return render(request, "custom_admin/sallers/index.html", {"sellers": sellers})




@admin_login_required
def create_seller(request):
    try:
        if request.method == "POST":
            form = SellerForm(request.POST, request.FILES)
            if form.is_valid():
                seller = form.save(commit=False)
                # Set default compliance_status
                seller.compliance_status = "pending"
                seller.save()
                messages.success(request, "Seller added successfully!")
                # Reset the form after saving
                form = SellerForm()
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = SellerForm()
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        form = SellerForm()
    
    return render(request, "custom_admin/sallers/sellers_create.html", {"form": form})




@admin_login_required
def seller_show(request, id):
    seller = get_object_or_404(Seller, id=id)
    return render(request, "custom_admin/sallers/seller_show.html", {"seller": seller})



@admin_login_required
def edit_seller(request, id):
    seller = Seller.objects.get(id=id)
    form = SellerForm(request.POST or None, instance=seller)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('custom_admin:admin_sellers_index')
    return render(request, "custom_admin/sallers/seller_edit.html", {"form": form, "seller": seller})



@admin_login_required
def update_seller(request, id):
    seller = get_object_or_404(Seller, id=id)
    
    if request.method == "POST":
        seller.name = request.POST.get('name')
        seller.contact_person = request.POST.get('contact_person')
        seller.email = request.POST.get('email')
        seller.phone = request.POST.get('phone')
        seller.save()
        messages.success(request, "Seller updated successfully!")
        return redirect('custom_admin:admin_sellers_index')

    return render(request, 'custom_admin/sallers/edit.html', {'seller': seller})



@admin_login_required
def delete_seller(request, id):
    try:
        seller = Seller.objects.get(id=id)
        seller.delete()
        messages.success(request, "Seller deleted successfully.")
    except Seller.DoesNotExist:
        messages.error(request, "Seller not found.")
    return redirect('custom_admin:admin_sellers_index')



@admin_login_required
def approve_seller(request, id):
    seller = get_object_or_404(Seller, id=id)
    seller.compliance_status = 'verified'
    seller.save()
    messages.success(request, "Seller approved successfully.")
    return redirect('custom_admin:admin_sellers_index')




@admin_login_required
def reject_seller(request, id):
    seller = get_object_or_404(Seller, id=id)
    seller.compliance_status = 'rejected'
    seller.save()
    messages.error(request, "Seller rejected successfully.")
    return redirect('custom_admin:admin_sellers_index')



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