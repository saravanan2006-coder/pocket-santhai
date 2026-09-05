# Pocketசந்தை (PocketSanthai) — Administrator & Developer Manual

This manual provides instructions for administrators managing the platform and developers maintaining the codebase.

---

## 1. System Overview & Architecture

Pocketசந்தை is a B2B wholesale marketplace built with Django 5.2 and Python 3.11.

- **Models**: `CustomUser`, `SellerProfile`, `StockItem`, `Bookmark`, `EmailVerificationToken`
- **Authentication**: Role-based (`seller` / `retailer`) with email verification and rate-limiting (`django-ratelimit`)
- **Background Tasks**: Celery with Redis/Valkey for asynchronous email dispatch
- **Static Assets**: WhiteNoise compressed manifest storage

---

## 2. User Roles & Access Control

| Role | Permissions & Capabilities | Access Level |
| :--- | :--- | :--- |
| **Wholesale Seller** | Can access `/seller/dashboard/`, `/seller/add-stock/`, `/seller/bulk-upload/`, `/seller/profile/`. Can create, edit, delete own stock. Cannot access retailer-exclusive actions. | Requires `email_verified = True` |
| **Retailer** | Can access `/search/`, `/bookmarks/`, `/compare/`. Can bookmark products and compare items. Cannot access seller dashboard or modify inventory. | Requires `email_verified = True` |
| **Superuser / Admin** | Access to `/admin/` panel with full CRUD over all users, tokens, profiles, stock items, and bookmarks. | Requires `is_superuser = True` |

---

## 3. Administrator Operations

### Accessing the Admin Panel
Navigate to `https://<domain>/admin/` and log in with your superuser credentials.

### Common Admin Tasks:
1. **Manual Email Verification**:
   If a user is unable to receive email, open **Custom users** → Select user → Check **Email verified** → Click **Save**.
2. **Assigning or Changing User Roles**:
   Open **Custom users** → Change **Role** to `seller` or `retailer`.
   - If switching to `seller`, ensure a corresponding entry exists in **Seller profiles**.
3. **Managing Stock Items**:
   Search and filter items by category or seller under **Stock items**.
4. **Monitoring Verification Tokens**:
   View active tokens under **Email verification tokens**. Expired tokens (>24h) are automatically cleaned up when accessed.

---

## 4. Developer Guide & Local Setup

### Initial Setup:
```bash
# 1. Clone repository & enter directory
git clone https://github.com/saravanan2006-coder/pocket-santhai.git
cd wholesale_marketplace

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Run tests
python manage.py test

# 6. Start development server
python manage.py runserver
```

### Email Verification in Dev Mode:
When `DJANGO_DEBUG=True`, email verification links are printed directly to the UI message alert upon registration or login attempts, and emails are saved to the `sent_emails/` folder.

---

## 5. Bulk Upload Format (.xlsx)

Wholesalers can upload stock items in bulk using an Excel spreadsheet (`.xlsx`).

### Required Columns (Row 1 Header):
| Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 (Optional) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Name** | **Category** | **Price** | **Unit** | **Quantity** | **Description** |
| Ponni Rice | Groceries | 52.00 | kg | 500 | 25kg bulk bag, Grade A |
| Sunflower Oil | Groceries | 115.50 | liter | 200 | 15 liter tin |

- Max rows per upload: **2,000 rows**.
- Price and Quantity must be non-negative numbers.

---

## 6. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'anymail'`
- **Cause**: Dependencies not installed in the active virtual environment.
- **Fix**: Run `pip install -r requirements.txt`.

### Issue: Celery Worker Connection Errors
- **Cause**: Redis / Valkey server not running or connection URL invalid.
- **Note**: Verification emails will automatically fall back to synchronous delivery if the Celery broker is unavailable.

### Issue: Rate Limit Exceeded (HTTP 403)
- **Cause**: Exceeded 5 login/registration requests per minute from the same IP.
- **Fix**: Wait 60 seconds or disable locally by setting `RATELIMIT_ENABLE=False` in `.env`.
