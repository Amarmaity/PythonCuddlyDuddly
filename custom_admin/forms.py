# custom_admin/forms.py
from django import forms
from api.models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "name", "contact_person", "email", "phone", "address", "city",
            "state", "country", "postal_code", "gst_number", "pan_number",
            "bank_account_number", "bank_name", "ifsc_code", "upi_id",
            "compliance_status", "bank_verified", "logo", "documents",
            "commission_rate", "is_active"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get("compliance_status"):
            self.initial["compliance_status"] = "pending" 
