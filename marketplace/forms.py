import re
import dns.resolver
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, StockItem, SellerProfile

DISPOSABLE_DOMAINS = {
    'mailinator.com', 'guerrillamail.com', 'tempmail.com', 'tempmail.net',
    '10minutemail.com', 'throwawaymail.com', 'sharklasers.com',
    'yopmail.com', 'trashmail.com', 'maildrop.cc', 'getairmail.com',
    'mailnator.com', 'spam4.me', 'spambox.us', 'temp-mail.org',
    'fakeinbox.com', 'mailexpire.com', 'mailmetrash.com',
}

ROLE_BASED_PREFIXES = ('admin@', 'info@', 'contact@', 'support@', 'noreply@', 'help@', 'webmaster@')

def validate_email_strict(value):
    domain = value.split('@')[1].lower() if '@' in value else ''

    if domain in DISPOSABLE_DOMAINS:
        raise ValidationError('Disposable email addresses are not allowed. Please use a permanent email.')

    if any(value.startswith(p) for p in ROLE_BASED_PREFIXES):
        raise ValidationError('Please use a personal email address, not a role-based one.')

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'style': 'display:flex;gap:1rem;'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Create a strong password (min 8 chars)'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required.')

        validate_email_strict(email)

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')

        return email

class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['name', 'category', 'price', 'unit', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Rice, Sugar, Oil'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Groceries, Spices'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kg, piece, liter'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['business_name', 'address', 'district', 'phone', 'email']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class BulkUploadForm(forms.Form):
    file = forms.FileField(
        label='Select an Excel file',
        help_text='Only .xlsx files are supported.',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx'})
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.xlsx'):
                raise ValidationError('Only .xlsx files are supported.')
        return file
