from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import StockItem, SellerProfile
from .forms import StockItemForm, SellerProfileForm

PAGE_SIZE = 20

def is_seller(user):
    return user.role == 'seller'

@login_required
@user_passes_test(is_seller, login_url='home')
def seller_dashboard(request):
    items = StockItem.objects.filter(seller=request.user).select_related('seller').order_by('-created_at')
    paginator = Paginator(items, PAGE_SIZE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'sellers/dashboard.html', {'page_obj': page_obj, 'items': page_obj.object_list})

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

import openpyxl
from decimal import Decimal

@login_required
@user_passes_test(is_seller, login_url='home')
def bulk_upload_stock(request):
    from .forms import BulkUploadForm
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            try:
                wb = openpyxl.load_workbook(excel_file, data_only=True)
                sheet = wb.active
                
                items_to_create = []
                errors = []
                row_num = 1
                
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    row_num += 1
                    if not any(row):
                        continue
                        
                    if len(row) < 5:
                        errors.append(f"Row {row_num}: Missing columns.")
                        continue
                        
                    name, category, price, unit, quantity = row[0], row[1], row[2], row[3], row[4]
                    description = row[5] if len(row) > 5 else ''
                    
                    if not all([name, category, price, unit, quantity]):
                        errors.append(f"Row {row_num}: Missing required fields.")
                        continue
                    
                    try:
                        price_val = Decimal(str(price))
                        quantity_val = int(quantity)
                    except (ValueError, TypeError, Exception):
                        errors.append(f"Row {row_num}: Invalid price or quantity format.")
                        continue
                    
                    items_to_create.append(
                        StockItem(
                            seller=request.user,
                            name=str(name).strip(),
                            category=str(category).strip(),
                            price=price_val,
                            unit=str(unit).strip(),
                            quantity=quantity_val,
                            description=str(description).strip() if description else ''
                        )
                    )
                
                if items_to_create:
                    StockItem.objects.bulk_create(items_to_create)
                    messages.success(request, f'Successfully added {len(items_to_create)} items!')
                
                if errors:
                    for error in errors[:5]:
                        messages.error(request, error)
                    if len(errors) > 5:
                        messages.error(request, f"...and {len(errors) - 5} more errors.")
                
                if not errors and not items_to_create:
                    messages.warning(request, 'No valid data found in the file.')
                    
                return redirect('seller_dashboard')
            except Exception as e:
                messages.error(request, f"Error reading Excel file: {str(e)}")
                return redirect('bulk_upload_stock')
    else:
        form = BulkUploadForm()
        
    return render(request, 'sellers/bulk_upload.html', {'form': form})
