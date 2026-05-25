<p align="center">
  <a href="#">
    <samp>
      <img alt="சந்தை" width="256" height="auto" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='256' height='80'%3E%3Ctext x='50%25' y='50%25' dominant-baseline='central' text-anchor='middle' font-family='serif' font-size='48' fill='%23A84331' font-weight='bold'%3Eசந்தை%3C/text%3E%3C/svg%3E">
    </samp>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-Supported-blue?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLite-Default-orange?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Deploy-Render.com-purple?style=for-the-badge&logo=render&logoColor=white" alt="Render">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge" alt="License">
</p>

<h1 align="center">சந்தை — பேரங்காடி.com</h1>

<p align="center">
  <strong>Tamil Nadu's Premier B2B Wholesale Marketplace</strong><br>
  <em>Connecting Wholesalers &amp; Retailers Across 38 Districts</em>
</p>

<p align="center">
  <samp>
    <a href="#-about">About</a> •
    <a href="#-features">Features</a> •
    <a href="#-getting-started">Quick Start</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-deployment">Deployment</a> •
    <a href="#-screenshots">Screenshots</a>
  </samp>
</p>

---

## 🧭 About

**சந்தை (Santhai)** — literally *"marketplace"* in Tamil — is a full-stack B2B web application built with Django that bridges the gap between **wholesale sellers** and **retailers** across all **38 districts of Tamil Nadu**.

Wholesalers upload their stock, manage their business profiles, and become discoverable. Retailers search products, compare prices across agencies, bookmark favorites, and contact suppliers directly.

---

## ✨ Features

### 🔐 Authentication & Security
| Feature | Description |
|---------|-------------|
| **Role-Based Accounts** | Register as Wholesale Seller or Retailer |
| **Email Verification** | UUID-based token system; blocks unverified logins |
| **Resend Verification** | One-click email resend from warning banner |
| **Admin Panel** | Full Django admin with custom user management |

### 🏪 For Wholesellers
| Feature | Description |
|---------|-------------|
| **Stock Management** | Add, edit, delete stock items with full details |
| **Business Profile** | Set business name, address, district, phone, email |
| **Dashboard** | Clean table view of all stock with quick actions |

### 🛒 For Retailers
| Feature | Description |
|---------|-------------|
| **Smart Search** | Search by item name, category, or description |
| **District Filter** | Filter by all 38 Tamil Nadu districts |
| **Category Filter** | Narrow down by product category |
| **Zero-Noise Results** | Only shows results when you actively search |
| **Supplier Contact** | Direct phone, email, address, and district info |

### 📌 Bookmark System
| Feature | Description |
|---------|-------------|
| **Save Favorites** | One-click bookmark on any search result |
| **Bookmarks Page** | Dedicated page to view all saved items |
| **Persistent** | Bookmarks tied to user account across sessions |
| **Quick Remove** | Delete bookmarks directly from the list |

### 📊 Comparison Table
| Feature | Description |
|---------|-------------|
| **Multi-Select** | Check 2+ items from search results |
| **Side-by-Side View** | Compare price, stock, seller, contact, district |
| **Smart Counter** | Live count of selected items |
| **From Bookmarks** | Compare directly from saved items page |

### 🎨 Design & Branding
| Element | Detail |
|---------|--------|
| **Bilingual UI** | Tamil (Mukta Malar) + English (Plus Jakarta Sans) |
| **Brand** | பேரங்காடி.com with "சந்தை" hero |
| **Color Palette** | Mustard (#D59A2B), Terracotta (#A84331), Earth Brown (#6D432A) |
| **SVG Illustrations** | Custom cartoon merchants, delivery trucks, storefronts |
| **Responsive** | Mobile-friendly with graceful degradation |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip & venv
- SQLite (default) or PostgreSQL (production)

### Installation

```bash
# 1. Clone & navigate
cd wholesale_marketplace

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

> 🌐 Open **http://localhost:8000** in your browser

---

## 🏗️ Architecture

### Tech Stack
```
┌─────────────────────────────────────────────┐
│                 Frontend                     │
│  HTML5 • CSS3 • SVG Illustrations            │
│  Plus Jakarta Sans + Mukta Malar Fonts       │
├─────────────────────────────────────────────┤
│                 Backend                      │
│  Django 5.0 • Python 3.11                    │
│  Custom User Model • Email Verification      │
├─────────────────────────────────────────────┤
│               Database                       │
│  SQLite (dev) → PostgreSQL (prod)            │
├─────────────────────────────────────────────┤
│               Deployment                     │
│  Render.com • Gunicorn • WhiteNoise          │
└─────────────────────────────────────────────┘
```

### Project Structure
```
wholesale_marketplace/
├── manage.py
├── requirements.txt
├── Procfile                      # Gunicorn config
├── render.yaml                   # One-click deploy
├── runtime.txt                   # Python version
├── .env.example                  # Env vars template
├── .gitignore
├── DEPLOY.md                     # Deployment guide
├── MANUAL.md                     # Admin & dev manual
└── marketplace/
    ├── settings.py               # Env-based config
    ├── urls.py                   # 17 URL routes
    ├── wsgi.py                   # Production server
    ├── models.py                 # 5 models
    ├── forms.py                  # 3 form classes
    ├── admin.py                  # 5 admin registrations
    ├── views_auth.py             # Login, register, email verify
    ├── views_sellers.py          # Stock CRUD, profile
    ├── views_retailers.py        # Search, bookmarks, compare
    └── templates/
        ├── base.html             # Master layout + navbar
        ├── marketplace/home.html # Landing page
        ├── registration/
        │   ├── login.html
        │   └── register.html
        ├── sellers/
        │   ├── dashboard.html
        │   ├── add_stock.html
        │   ├── edit_stock.html
        │   └── profile.html
        └── retailers/
            ├── search.html       # Search + bookmark + compare
            ├── bookmarks.html    # Saved items
            └── compare.html      # Side-by-side table
```

### Database Models
```
CustomUser ────────────────────────── Base user (seller/retailer)
    │
    ├── email_verified ────────────── Boolean flag
    │
    ├── SellerProfile ─────────────── Business details (1:1)
    │   ├── business_name, address
    │   ├── district (38 TN options)
    │   ├── phone, email
    │
    ├── StockItem ─────────────────── Products (1:N seller)
    │   ├── name, category, price
    │   ├── unit, quantity
    │   └── description
    │
    ├── Bookmark ──────────────────── Saved items (1:N user)
    │   └── item (FK to StockItem)
    │
    └── EmailVerificationToken ────── UUID tokens (1:N user)
```

---

## 🖼️ Screenshots

### Landing Page
```
┌─────────────────────────────────────────────────────────┐
│  பேரங்காடி.com                    [Login] [Register]      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   [Illustration]      சந்தை        [Illustration]      │
│                    தமிழ்நாட்டின் மொத்த                  │
│                     விற்பனை மையம்                     │
│                                                         │
│          ┌─────────────────────────────────┐            │
│          │ 🔍 Search Products / தேடல்... │ [தேடல்] │            │
│          └─────────────────────────────────┘            │
│                                                         │
├─────────────────────┬───────────────────────────────────┤
│   Wholesalers       │       Retailers                   │
│   கொள்முதல்காரர்கள்  │  சில்லறை விற்பனையாளர்கள்         │
│   [Desk Illustration] │  [Store Illustration]           │
│   [மேலாண்மை சரக்கு]    │  [இப்போது தேடவும்]              │
├─────────────────────┼───────────────────────────────────┤
│  ஸ்மார்ட் தேடல்     │  மாவட்ட வடிகட்டி  │ நேரடி தொடர்பு │
│  Smart Search       │  District Filter  │ Direct Contact │
└─────────────────────┴───────────────────────────────────┘
```

### Search Results
```
┌─────────────────────────────────────────────────────────┐
│  🔍 தேடல் - Find Products Across Tamil Nadu Wholesalers │
├─────────────────────────────────────────────────────────┤
│  [Search Item]  [District ▾]  [Category ▾]  [தேடல்]     │
├─────────────────────────────────────────────────────────┤
│  ☑ Select items to compare: 0 selected  [Compare ▸]    │
├─────────────────────────────────────────────────────────┤
│  ┌─ Rice ─────────────────────── ₹25/kg ──────────────┐ │
│  │  Groceries  |  Stock: 500                          │ │
│  │  📍 Anna Wholesale, Chennai | District: Chennai    │ │
│  │  📞 9876543210 | ✉ anna@wholesale.com              │ │
│  │                              [☑ Compare] [🔖 Save]  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🌍 Deployment

### Environment Variables
```
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=wholesale_db
DATABASE_USER=wholesale_user
DATABASE_PASSWORD=<your-password>
DATABASE_HOST=<your-host>
DATABASE_PORT=5432
```

### Render.com (One-Click)
1. Push to GitHub
2. Go to [render.com](https://render.com) → **New Blueprint**
3. Connect your repo — `render.yaml` auto-configures everything

> 📖 Full guide: [`DEPLOY.md`](DEPLOY.md)

---

## 📋 Tamil Nadu Districts Covered

<details>
<summary>All 38 districts (click to expand)</summary>

Ariyalur · Chengalpattu · Chennai · Coimbatore · Cuddalore · Dharmapuri · Dindigul · Erode · Kallakurichi · Kanchipuram · Kanyakumari · Karur · Krishnagiri · Madurai · Mayiladuthurai · Nagapattinam · Namakkal · Nilgiris · Perambalur · Pudukkottai · Ramanathapuram · Ranipet · Salem · Sivaganga · Tenkasi · Thanjavur · Theni · Thoothukudi · Tiruchirappalli · Tirunelveli · Tirupattur · Tiruppur · Tiruvallur · Tiruvannamalai · Tiruvarur · Vellore · Villupuram · Virudhunagar

</details>

---

## 📄 License

MIT License — Free for personal and commercial use.

---

<p align="center">
  <sub>Built with ❤️ for Tamil Nadu's wholesale community</sub><br>
  <samp>© 2026 சந்தை பேரங்காடி.com</samp>
</p>
