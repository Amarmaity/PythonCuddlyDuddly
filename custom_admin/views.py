from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from api.models import Seller, User
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger

from custom_admin.emails import send_approval_email, send_rejection_email
from .decorators import admin_login_required
from custom_admin.forms import SellerForm
from http import HTTPStatus 
from django.http import FileResponse, Http404
import os
# Create your views here.

def admin_dashboard(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return redirect("api:login")
    admin_user = User.objects.get(id=admin_id)
    return render(request, "custom_admin/adminDashboard.html", {"admin_user": admin_user})




@admin_login_required
def saller_index(request):
    try:
        sellers = Seller.objects.filter(compliance_status='verified')

        # --- Search ---
        search = request.GET.get('search')
        if search:
            sellers = sellers.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        # --- Status Filter ---
        status = request.GET.get('status')
        if status == '1':
            sellers = sellers.filter(is_active=True)
        elif status == '0':
            sellers = sellers.filter(is_active=False)

        # --- Sort ---
        sort = request.GET.get('sort')
        if sort == 'latest':
            sellers = sellers.order_by('-created_at')
        elif sort == 'oldest':
            sellers = sellers.order_by('created_at')
        elif sort == 'name':
            sellers = sellers.order_by('name')

        # --- Pagination ---
        paginator = Paginator(sellers, 10)
        page_number = request.GET.get('page')

        try:
            sellers_page = paginator.get_page(page_number)
        except (EmptyPage, PageNotAnInteger):
            sellers_page = paginator.get_page(1)

        # --- Render Success ---
        return render(request,"custom_admin/sallers/index.html",{"sellers": sellers_page},status=HTTPStatus.OK)

    except Exception as e:
        # --- Catch unexpected errors ---
        return JsonResponse({"error": str(e)},status=HTTPStatus.INTERNAL_SERVER_ERROR)



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
def download_docs(request, id):
    # Correctly pass id as a keyword argument
    seller = get_object_or_404(Seller, pk=id)

    # Check if document exists
    if not seller.documents:
        raise Http404("No documents found for this seller.")
    
    file_path = seller.documents.path
    if not os.path.exists(file_path):
        raise Http404("Document file not found on server.")

    # Return the file as an attachment
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))



@admin_login_required
def view_docs(request, id):
    seller = get_object_or_404(Seller, pk=id)

    # Check if document exists
    if not seller.documents:
        raise Http404("No documents found for this seller.")
    
    file_path = seller.documents.path
    if not os.path.exists(file_path):
        raise Http404("Document file not found on server.")

    # Serve the file inline (browser will try to open it)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response



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
    seller = get_object_or_404(Seller, pk=id)
    seller.compliance_status = 'verified'
    seller.save()

    send_approval_email(seller.email, seller.name)
    messages.success(request, f"Seller {seller.name} has been approved.")
    return redirect('custom_admin:admin_sellers_index')


@admin_login_required
def reject_seller(request, id):
    if request.method == "POST":
        seller = get_object_or_404(Seller, id=id)
        reason = request.POST.get("rejection_reason")

        if reason:
            seller.compliance_status = "rejected"
            seller.rejection_reason = reason
            seller.save()

            # ✅ Correct email function
            send_rejection_email(seller.email, seller.name, reason)

            messages.success(request, f"Seller {seller.name} has been rejected.")
        else:
            messages.error(request, "Rejection reason is required.")
    
    return redirect("custom_admin:kyc_compliance")





@admin_login_required
def saller_application(request):

    return render(request, "custom_admin/sallers/sellers_create.html")


@admin_login_required
def kyc_compliance(request):
    # Separate pending and rejected sellers
    pending_sellers = Seller.objects.filter(compliance_status='pending', is_active=True).order_by('-created_at')
    rejected_sellers = Seller.objects.filter(compliance_status='rejected', is_active=True).order_by('-updated_at')

    # Pagination for both tabs (optional)
    pending_page = request.GET.get('page', 1)
    rejected_page = request.GET.get('rejected_page', 1)

    pending_paginator = Paginator(pending_sellers, 10)  # 10 per page
    rejected_paginator = Paginator(rejected_sellers, 10)

    pendingKyc = pending_paginator.get_page(pending_page)
    rejectedKyc = rejected_paginator.get_page(rejected_page)

    context = {
        'pendingKyc': pendingKyc,
        'rejectedKyc': rejectedKyc,
    }
    return render(request, "custom_admin/sallers/kyc_compliance.html", context)


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