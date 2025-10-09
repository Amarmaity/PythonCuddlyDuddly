from enum import unique
from os import name
from pyclbr import Class
from pyexpat import model
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
from numpy import mod
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
    

class Seller(models.Model):
    COMPLIANCE_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True, blank=False, null=False)

    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    gst_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    pan_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    ifsc_code = models.CharField(max_length=50, null=True, blank=True)
    upi_id = models.CharField(max_length=50, null=True, blank=True)

    compliance_status = models.CharField(max_length=10, choices=COMPLIANCE_STATUS, default='pending', null=True, blank=True)
    bank_verified = models.BooleanField(default=False)

    logo = models.CharField(max_length=255, null=True, blank=True)
    documents = models.CharField(max_length=255, null=True, blank=True)

    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_seller"

    def __str__(self):
        return f"{self.contact_person} ({self.name}) - {self.email}"