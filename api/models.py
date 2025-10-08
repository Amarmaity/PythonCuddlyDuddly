from enum import unique
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password, check_password as django_check_password




# Create your models here.
class MasterProduct(models.Model):
    name = models.CharField(max_length=100,default="temp-name")
    slug = models.CharField(max_length=100, unique=True, default="temp-slug")
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



# Category table
class Category(models.Model):
    name = models.CharField(max_length=100,default="temp-name")
    slug = models.CharField(max_length=100, unique=True, default="temp-slug")
    description = models.TextField(null=True)
    image_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(models.Model):
    USER_TYPES = [
        ("admin", "Admin"),
        ("super_admin", "Super Admin"),
        ("vendor", "Vendor"),
        ("customer", "Customer"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES) 
    phone = PhoneNumberField(("Phone number"), unique=True, blank=False, null=False)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'api_user'

    def set_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.email})"
