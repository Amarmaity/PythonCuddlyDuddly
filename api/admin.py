from django.contrib import admin
from .models import Category, MasterProduct, Seller, User
# Register your models here.

admin.site.register(MasterProduct)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Seller)