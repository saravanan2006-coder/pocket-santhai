from django.contrib import admin
from .models import CustomUser, SellerProfile, StockItem

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active')

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'district', 'phone')
    list_filter = ('district',)

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'quantity', 'created_at')
    list_filter = ('category', 'seller')
    search_fields = ('name', 'category')
