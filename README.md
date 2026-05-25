# TN Wholesale Marketplace

A B2B platform connecting wholesale sellers with retailers across Tamil Nadu.

## Features

- **User Authentication** - Register as Wholesale Seller or Retailer
- **Seller Dashboard** - Upload, edit, and manage stock items
- **Seller Profile** - Business name, address, district, and contact info
- **Product Search** - Search by item name, category, or description
- **District Filter** - Filter results by all 38 districts of Tamil Nadu
- **Contact Info** - View wholesaler address, phone, and email in results

## Quick Start

```bash
cd wholesale_marketplace
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://localhost:8000

## User Flow

### For Wholesale Sellers
1. Register with role "Wholesale Seller"
2. Set up your business profile (name, address, district, phone)
3. Add stock items from the dashboard
4. Retailers will see your contact info when they search your products

### For Retailers
1. Register with role "Retailer"
2. Go to Search page
3. Enter item name (e.g., "Rice", "Sugar")
4. Optionally filter by district or category
5. View results with wholesaler names, prices, contact details, and addresses

## Project Structure

```
wholesale_marketplace/
├── manage.py
├── requirements.txt
└── marketplace/
    ├── settings.py
    ├── urls.py
    ├── models.py          # CustomUser, SellerProfile, StockItem
    ├── forms.py           # Registration, Stock, Profile forms
    ├── views_auth.py      # Login, Register, Home
    ├── views_sellers.py   # Seller dashboard, CRUD for stock
    ├── views_retailers.py # Search with filters
    └── templates/
        ├── base.html
        ├── marketplace/home.html
        ├── registration/
        │   ├── login.html
        │   └── register.html
        ├── sellers/
        │   ├── dashboard.html
        │   ├── add_stock.html
        │   ├── edit_stock.html
        │   └── profile.html
        └── retailers/
            └── search.html
```

## Database

Defaults to SQLite for development. For production with PostgreSQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wholesale_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Tamil Nadu Districts

All 38 districts: Ariyalur, Chengalpattu, Chennai, Coimbatore, Cuddalore, Dharmapuri, Dindigul, Erode, Kallakurichi, Kanchipuram, Kanyakumari, Karur, Krishnagiri, Madurai, Mayiladuthurai, Nagapattinam, Namakkal, Nilgiris, Perambalur, Pudukkottai, Ramanathapuram, Ranipet, Salem, Sivaganga, Tenkasi, Thanjavur, Theni, Thoothukudi, Tiruchirappalli, Tirunelveli, Tirupattur, Tiruppur, Tiruvallur, Tiruvannamalai, Tiruvarur, Vellore, Villupuram, Virudhunagar.
