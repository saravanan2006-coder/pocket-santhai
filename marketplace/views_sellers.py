from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import StockItem, SellerProfile
from .forms import StockItemForm, SellerProfileForm

def is_seller(user):
    return user.role == 'seller'

@login_required
@user_passes_test(is_seller, login_url='home')
def seller_dashboard(request):
    items = StockItem.objects.filter(seller=request.user)
    return render(request, 'sellers/dashboard.html', {'items': items})

@login_required
@user_passes_test(is_seller, login_url='home')
def add_stock(request):
    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, 'Stock item added successfully!')
            return redirect('seller_dashboard')
    else:
        form = StockItemForm()
    return render(request, 'sellers/add_stock.html', {'form': form})

@login_required
@user_passes_test(is_seller, login_url='home')
def edit_stock(request, pk):
    item = get_object_or_404(StockItem, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock item updated successfully!')
            return redirect('seller_dashboard')
    else:
        form = StockItemForm(instance=item)
    return render(request, 'sellers/edit_stock.html', {'form': form, 'item': item})

@login_required
@user_passes_test(is_seller, login_url='home')
def delete_stock(request, pk):
    item = get_object_or_404(StockItem, pk=pk, seller=request.user)
    item.delete()
    messages.success(request, 'Stock item deleted successfully!')
    return redirect('seller_dashboard')

@login_required
@user_passes_test(is_seller, login_url='home')
def seller_profile(request):
    profile, created = SellerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('seller_profile')
    else:
        form = SellerProfileForm(instance=profile)
    return render(request, 'sellers/profile.html', {'form': form})
