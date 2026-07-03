from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import StockItem, TN_DISTRICTS, Bookmark

PAGE_SIZE = 20

def search(request):
    query = request.GET.get('q', '').strip()
    district = request.GET.get('district', '')
    category = request.GET.get('category', '')

    items = StockItem.objects.none()

    if query or district or category:
        items = StockItem.objects.select_related('seller', 'seller__seller_profile').all()
        if query:
            items = items.filter(
                Q(name__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query)
            )
        if district:
            items = items.filter(seller__seller_profile__district=district)
        if category:
            items = items.filter(category__icontains=category)

    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('item_id', flat=True)
        )

    categories = StockItem.objects.values_list('category', flat=True).distinct()

    paginator = Paginator(items, PAGE_SIZE) if items else None
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number) if paginator else None

    context = {
        'items': page_obj.object_list if page_obj else items,
        'page_obj': page_obj,
        'query': query,
        'district': district,
        'category': category,
        'districts': TN_DISTRICTS,
        'categories': categories,
        'bookmarked_ids': bookmarked_ids,
    }
    return render(request, 'retailers/search.html', context)

@login_required
def toggle_bookmark(request, item_id):
    item = get_object_or_404(StockItem, pk=item_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, item=item)
    if not created:
        bookmark.delete()
        messages.info(request, f'Removed "{item.name}" from bookmarks.')
    else:
        messages.success(request, f'Bookmarked "{item.name}"!')
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'search'
    return redirect(next_url)

@login_required
def bookmarks_view(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('item', 'item__seller', 'item__seller__seller_profile')
    return render(request, 'retailers/bookmarks.html', {'bookmarks': bookmarks})

@login_required
def compare_view(request):
    item_ids = request.GET.getlist('items')
    if not item_ids:
        messages.warning(request, 'Please select at least 2 items to compare.')
        return redirect('search')
    items = StockItem.objects.filter(pk__in=item_ids).select_related('seller', 'seller__seller_profile')
    if len(items) < 2:
        messages.warning(request, 'Select at least 2 items to compare.')
        return redirect('search')
    return render(request, 'retailers/compare.html', {'items': items})
