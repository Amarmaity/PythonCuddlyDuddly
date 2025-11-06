from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.validators import FileExtensionValidator


# ----------------------------
# Custom User Manager
# ----------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "super_admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# ----------------------------
# Custom User Model
# ----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone", "user_type"]

    class Meta:
        db_table = "api_user"

    def __str__(self):
        return f"{self.name} ({self.email})"


# ----------------------------
# Seller Model
# ----------------------------
class Seller(models.Model):
    COMPLIANCE_STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)

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
    rejection_reason = models.TextField(null=True, blank=True)
    bank_verified = models.BooleanField(default=False)

    logo = models.ImageField(
        upload_to="sellers/logos/", null=True, blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    documents = models.FileField(
        upload_to="sellers/documents/", null=True, blank=True,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_sellers"

    def __str__(self):
        return f"{self.contact_person} ({self.name}) - {self.email}"


# ----------------------------
# Customer Model
# ----------------------------
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_customer"

    def __str__(self):
        return f"{self.user.name if self.user else 'Unknown'} ({self.user.email if self.user else ''})"


class Category(models.Model):
    name = models.CharField(max_length=100, default="temp-name")
    slug = models.CharField(max_length=100, unique=True, default="temp-slug")
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_category"

    def __str__(self):
        return self.name


class MasterProduct(models.Model):
    name = models.CharField(max_length=100, default="temp-name")
    slug = models.CharField(max_length=100, unique=True, default="temp-slug")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_masterproduct"

    def __str__(self):
        return self.name