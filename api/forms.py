from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["name", "email", "user_type", "phone"]

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don’t match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class UserLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)

from django import forms

class UserLoginForm(forms.Form):
    email_or_phone = forms.CharField(
        label="Email or Phone",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your email or phone number"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        email_or_phone = cleaned_data.get("email_or_phone")
        password = cleaned_data.get("password")

        if not email_or_phone:
            raise forms.ValidationError("Please enter your email or phone number.")
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return cleaned_data

