from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StockItem, SellerProfile, TN_DISTRICTS

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
            'password1': forms.PasswordInput(attrs={'placeholder': 'Create a strong password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

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
