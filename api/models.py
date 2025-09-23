from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone 

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






#







from django.db import models
from django.contrib.auth.hashers import make_password

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
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return f"{self.name} ({self.email})"
