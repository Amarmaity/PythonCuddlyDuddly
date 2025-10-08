from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('',views.admin_dashboard, name='adminDashboard'),
    # Sallers
    path('sellers/', views.saller_index, name='admin_sellers_index'),
    path('sellers-application/', views.saller_application, name='admin_seller_applications'),
    path('kyc-complince/', views.kyc_compliance, name='admin_sellers_compliance'),
    path('payout/', views.payout, name='admin_payouts'),

    # Products
    path('products/', views.product_index, name='admin_products_index'),
    path('category/', views.category_index, name='admin_categories_index'),

    # Coustomer
    path('customer/', views.customer_index, name='admin_customers_index'),
    path('customer-review/', views.review_index, name='admin_reviews_index'),

    # Reports
    path('sales-report/', views.report_sales, name='admin_reports_sales'),
    path('reports-revenue/', views.report_revenue, name='admin_reports_revenue'),
    path('reports-saller/', views.reports_saller, name='admin_reports_seller'),
    path('reports-customer/', views.report_customer, name='admin_reports_customer'),

    # Setting
    path('setting/', views.setting_index, name='admin_settings_general'),
    path('setting-payments/', views.setting_payment, name='admin_settings_payments'),
    path('setting-shipping/', views.setting_shipping, name='admin_settings_shipping'),
    path('roles-index', views.roles_indexinig, name='admin_roles_index'),

    




]
