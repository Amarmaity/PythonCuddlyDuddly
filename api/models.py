from ast import mod
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class MasterProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

def __str__(self):
    return self.name



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
