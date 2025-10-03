from django.contrib import admin
from .models import Category, MasterProduct, User
# Register your models here.

admin.site.register(MasterProduct)
admin.site.register(Category)
admin.site.register(User)