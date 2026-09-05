import io
import datetime
from decimal import Decimal
import openpyxl
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from .models import CustomUser, SellerProfile, StockItem, Bookmark, EmailVerificationToken, TN_DISTRICTS

@override_settings(RATELIMIT_ENABLE=False)
class ModelAndPropertyTests(TestCase):
    def setUp(self):
        self.seller_user = CustomUser.objects.create_user(
            username='seller1',
            email='seller1@domain.com',
            password='Password123!',
            role='seller',
            email_verified=True
        )
        self.profile = SellerProfile.objects.create(
            user=self.seller_user,
            business_name='Test Traders',
            address='123 Market St',
            district=TN_DISTRICTS[0],
            phone='9876543210',
            email='seller1@domain.com'
        )

    def test_stock_item_safe_seller_profile(self):
        item = StockItem.objects.create(
            seller=self.seller_user,
            name='Test Product',
            category='Groceries',
            price=Decimal('100.00'),
            unit='kg',
            quantity=50
        )
        self.assertIsNotNone(item.seller_profile)
        self.assertEqual(item.seller_profile.business_name, 'Test Traders')

        # Seller without profile should not crash item.seller_profile
        seller_no_profile = CustomUser.objects.create_user(
            username='seller2',
            email='seller2@domain.com',
            password='Password123!',
            role='seller',
            email_verified=True
        )
        item2 = StockItem.objects.create(
            seller=seller_no_profile,
            name='Test Product 2',
            category='Groceries',
            price=Decimal('50.00'),
            unit='kg',
            quantity=20
        )
        self.assertIsNone(item2.seller_profile)

    def test_token_expiration(self):
        token = EmailVerificationToken.objects.create(user=self.seller_user)
        self.assertFalse(token.is_expired)
        token.created_at = timezone.now() - datetime.timedelta(hours=25)
        token.save()
        self.assertTrue(token.is_expired)

@override_settings(RATELIMIT_ENABLE=False)
class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_creates_seller_profile_and_token(self):
        response = self.client.post(reverse('register'), {
            'username': 'newseller',
            'email': 'newseller@validemail.com',
            'role': 'seller',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'phone': '9876543210'
        })
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username='newseller')
        self.assertFalse(user.email_verified)
        self.assertTrue(SellerProfile.objects.filter(user=user).exists())
        self.assertTrue(EmailVerificationToken.objects.filter(user=user).exists())

    def test_login_blocked_if_unverified(self):
        user = CustomUser.objects.create_user(
            username='unverified_user',
            email='unverified@validemail.com',
            password='Password123!',
            role='retailer',
            email_verified=False
        )
        response = self.client.post(reverse('login'), {
            'username': 'unverified_user',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_verify_email_view(self):
        user = CustomUser.objects.create_user(
            username='user_to_verify',
            email='verify@validemail.com',
            password='Password123!',
            role='retailer',
            email_verified=False
        )
        token = EmailVerificationToken.objects.create(user=user)
        response = self.client.get(reverse('verify_email', args=[token.token]))
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.email_verified)

    def test_resend_verification_unauthenticated(self):
        user = CustomUser.objects.create_user(
            username='lost_token_user',
            email='lost@validemail.com',
            password='Password123!',
            role='retailer',
            email_verified=False
        )
        EmailVerificationToken.objects.create(user=user)
        response = self.client.get(reverse('resend_verification') + f'?email={user.email}')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EmailVerificationToken.objects.filter(user=user).exists())

@override_settings(RATELIMIT_ENABLE=False)
class SellerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller = CustomUser.objects.create_user(
            username='seller_boss',
            email='boss@validemail.com',
            password='Password123!',
            role='seller',
            email_verified=True
        )
        self.profile = SellerProfile.objects.create(
            user=self.seller,
            business_name='Boss Wholesale',
            address='Coimbatore Main Rd',
            district='Coimbatore',
            phone='9988776655'
        )
        self.client.force_login(self.seller)

    def test_add_and_edit_stock(self):
        response = self.client.post(reverse('add_stock'), {
            'name': 'Basmati Rice',
            'category': 'Rice & Grains',
            'price': '85.50',
            'unit': 'kg',
            'quantity': 100,
            'description': 'Premium long grain'
        })
        self.assertEqual(response.status_code, 302)
        item = StockItem.objects.get(name='Basmati Rice')
        self.assertEqual(item.seller, self.seller)

        # Edit item
        edit_response = self.client.post(reverse('edit_stock', args=[item.pk]), {
            'name': 'Basmati Rice Supreme',
            'category': 'Rice & Grains',
            'price': '90.00',
            'unit': 'kg',
            'quantity': 120,
            'description': 'Updated description'
        })
        self.assertEqual(edit_response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Basmati Rice Supreme')

    def test_delete_stock_post_only(self):
        item = StockItem.objects.create(
            seller=self.seller,
            name='Item to Delete',
            category='Category',
            price=Decimal('10.00'),
            unit='piece',
            quantity=5
        )
        # GET request should be rejected (405 Method Not Allowed)
        get_resp = self.client.get(reverse('delete_stock', args=[item.pk]))
        self.assertEqual(get_resp.status_code, 405)
        self.assertTrue(StockItem.objects.filter(pk=item.pk).exists())

        # POST request should succeed
        post_resp = self.client.post(reverse('delete_stock', args=[item.pk]))
        self.assertEqual(post_resp.status_code, 302)
        self.assertFalse(StockItem.objects.filter(pk=item.pk).exists())

    def test_bulk_upload_valid_and_invalid(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Name', 'Category', 'Price', 'Unit', 'Quantity', 'Description'])
        ws.append(['Bulk Item 1', 'Spices', '45.00', 'kg', '100', 'Good quality'])
        ws.append(['Bulk Item Negative', 'Spices', '-10.00', 'kg', '-5', 'Negative value'])

        excel_stream = io.BytesIO()
        wb.save(excel_stream)
        excel_stream.seek(0)
        excel_stream.name = 'test_upload.xlsx'

        response = self.client.post(reverse('bulk_upload_stock'), {'file': excel_stream})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(StockItem.objects.filter(name='Bulk Item 1').exists())
        self.assertFalse(StockItem.objects.filter(name='Bulk Item Negative').exists())

@override_settings(RATELIMIT_ENABLE=False)
class RetailerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.retailer = CustomUser.objects.create_user(
            username='retailer1',
            email='retailer1@validemail.com',
            password='Password123!',
            role='retailer',
            email_verified=True
        )
        self.seller = CustomUser.objects.create_user(
            username='seller_tn',
            email='sellertn@validemail.com',
            password='Password123!',
            role='seller',
            email_verified=True
        )
        self.profile = SellerProfile.objects.create(
            user=self.seller,
            business_name='Madurai Traders',
            address='Madurai Market',
            district='Madurai',
            phone='9123456780'
        )
        self.item1 = StockItem.objects.create(
            seller=self.seller,
            name='Tamil Ponni Rice',
            category='Grains',
            price=Decimal('42.00'),
            unit='kg',
            quantity=200
        )
        self.item2 = StockItem.objects.create(
            seller=self.seller,
            name='Red Chilli Guntur',
            category='Spices',
            price=Decimal('180.00'),
            unit='kg',
            quantity=50
        )
        self.client.force_login(self.retailer)

    def test_search_zero_noise_initially(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 0)

        # Search with keyword
        search_resp = self.client.get(reverse('search') + '?q=Ponni')
        self.assertEqual(search_resp.status_code, 200)
        self.assertEqual(len(search_resp.context['items']), 1)

    def test_toggle_bookmark_and_open_redirect_protection(self):
        response = self.client.post(
            reverse('toggle_bookmark', args=[self.item1.pk]),
            {'next': 'https://evil-attacker.com'}
        )
        self.assertEqual(response.status_code, 302)
        # Should NOT redirect to external malicious domain
        self.assertNotIn('evil-attacker.com', response.url)
        self.assertTrue(Bookmark.objects.filter(user=self.retailer, item=self.item1).exists())

    def test_compare_view_sanitization(self):
        # Invalid / non-integer ids
        resp_bad = self.client.get(reverse('compare') + '?items=abc&items=xyz')
        self.assertEqual(resp_bad.status_code, 302)

        # Valid items
        resp_good = self.client.get(reverse('compare') + f'?items={self.item1.pk}&items={self.item2.pk}')
        self.assertEqual(resp_good.status_code, 200)
        self.assertEqual(len(resp_good.context['items']), 2)
