from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views_auth import user_login, user_register, home, verify_email, resend_verification
from .views_sellers import seller_dashboard, add_stock, edit_stock, delete_stock, seller_profile
from .views_retailers import search, toggle_bookmark, bookmarks_view, compare_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', user_register, name='register'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('search/', search, name='search'),
    path('bookmark/<int:item_id>/', toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', bookmarks_view, name='bookmarks'),
    path('compare/', compare_view, name='compare'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/add-stock/', add_stock, name='add_stock'),
    path('seller/edit-stock/<int:pk>/', edit_stock, name='edit_stock'),
    path('seller/delete-stock/<int:pk>/', delete_stock, name='delete_stock'),
    path('seller/profile/', seller_profile, name='seller_profile'),
]
