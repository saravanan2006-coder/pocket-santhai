from django.contrib import admin
from .models import CustomUser, EmailVerificationToken, SellerProfile, StockItem, Bookmark

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'email_verified', 'is_active')
    list_filter = ('role', 'email_verified', 'is_active')

@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    list_filter = ('created_at',)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'district', 'phone')
    list_filter = ('district',)

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'quantity', 'created_at')
    list_filter = ('category', 'seller')
    search_fields = ('name', 'category')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'created_at')
    list_filter = ('created_at',)
