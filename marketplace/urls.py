from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from .views_auth import user_login, user_register, home, verify_email, resend_verification, privacy_policy, terms_and_conditions
from .views_sellers import seller_dashboard, add_stock, edit_stock, delete_stock, seller_profile, bulk_upload_stock
from .views_retailers import search, toggle_bookmark, bookmarks_view, compare_view

def health_check(request):
    return JsonResponse({'status': 'ok', 'service': 'wholesync'}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', user_register, name='register'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('privacy-policy', privacy_policy),
    path('terms-and-conditions/', terms_and_conditions, name='terms_and_conditions'),
    path('terms-and-conditions', terms_and_conditions),
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    path('verify-email/<str:token>', verify_email),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('search/', search, name='search'),
    path('bookmark/<int:item_id>/', toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', bookmarks_view, name='bookmarks'),
    path('compare/', compare_view, name='compare'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/add-stock/', add_stock, name='add_stock'),
    path('seller/bulk-upload/', bulk_upload_stock, name='bulk_upload_stock'),
    path('seller/edit-stock/<int:pk>/', edit_stock, name='edit_stock'),
    path('seller/delete-stock/<int:pk>/', delete_stock, name='delete_stock'),
    path('seller/profile/', seller_profile, name='seller_profile'),
]
