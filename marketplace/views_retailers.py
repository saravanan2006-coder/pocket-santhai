from django.shortcuts import render
from django.db.models import Q
from .models import StockItem, TN_DISTRICTS

def search(request):
    query = request.GET.get('q', '').strip()
    district = request.GET.get('district', '')
    category = request.GET.get('category', '')

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

    categories = StockItem.objects.values_list('category', flat=True).distinct()

    context = {
        'items': items,
        'query': query,
        'district': district,
        'category': category,
        'districts': TN_DISTRICTS,
        'categories': categories,
    }
    return render(request, 'retailers/search.html', context)
