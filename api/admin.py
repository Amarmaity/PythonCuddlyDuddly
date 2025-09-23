from django.contrib import admin
from .models import Category, MasterProduct
# Register your models here.

admin.site.register(MasterProduct)
admin.site.register(Category)