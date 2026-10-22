from unittest.mock import patch

from django.test import override_settings
from rest_framework.test import APITestCase

from market.models import Category, MarketItem
from notifications.models import Notification
from users.models import User


def make_user(phone, **extra):
    return User.objects.create_user(phone_number=phone, password='Str0ng-pass!', first_name='Ali', last_name='Valiyev', **extra)


class SecurityTestCase(APITestCase):
    """Ruxsatlar (permission) bo'yicha regressiya testlari."""

    def setUp(self):
        # Testlarda Google Translate'ga so'rov ketmasligi uchun
        patcher = patch('agroRent.utils.mixins.translate_text', side_effect=lambda text, lang='uz': text)
        patcher.start()
        self.addCleanup(patcher.stop)

        self.user = make_user('+998900000001')
        self.other = make_user('+998900000002')
        self.renter = make_user('+998900000003', is_renter=True)
        self.staff = make_user('+998900000004', is_staff=True)


class UserManagementTests(SecurityTestCase):
    def test_regular_user_cannot_create_users(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/users/list/', {
            'phone_number': '+998901111111', 'first_name': 'X', 'last_name': 'Y',
            'region': 'r', 'district': 'd', 'street': 's', 'house_number': '1',
            'is_superuser': True, 'is_staff': True,
        })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(User.objects.filter(phone_number='+998901111111').exists())

    def test_staff_cannot_grant_superuser_via_api(self):
        self.client.force_authenticate(self.staff)
        response = self.client.post('/api/users/list/', {
            'phone_number': '+998901111112', 'first_name': 'X', 'last_name': 'Y',
            'region': 'r', 'district': 'd', 'street': 's', 'house_number': '1',
            'is_superuser': True, 'is_staff': True, 'password': 'Str0ng-pass!',
        })
        self.assertEqual(response.status_code, 201)
        created = User.objects.get(phone_number='+998901111112')
        self.assertFalse(created.is_superuser)
        self.assertFalse(created.is_staff)
        self.assertTrue(created.check_password('Str0ng-pass!'))

    def test_user_detail_is_staff_only(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.patch(f'/api/users/list/{self.other.pk}/', {'first_name': 'Hack'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/users/list/{self.other.pk}/').status_code, 403)

        self.client.force_authenticate(self.staff)
        response = self.client.patch(f'/api/users/list/{self.other.pk}/', {'first_name': 'Yangi', 'is_superuser': True})
        self.assertEqual(response.status_code, 200)
        self.other.refresh_from_db()
        self.assertEqual(self.other.first_name, 'Yangi')
        self.assertFalse(self.other.is_superuser)


class NotificationTests(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.own = Notification.objects.create(user=self.user, title='Mening', description='d')
        self.foreign = Notification.objects.create(user=self.other, title='Begona', description='d')

    def test_cannot_access_other_users_notification(self):
        self.client.force_authenticate(self.user)
        url = f'/api/notifications/list/{self.foreign.pk}/'
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)
        self.assertTrue(Notification.objects.filter(pk=self.foreign.pk).exists())

    def test_owner_can_read_and_delete_but_not_edit(self):
        self.client.force_authenticate(self.user)
        url = f'/api/notifications/list/{self.own.pk}/'
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.patch(url, {'user': self.other.pk}).status_code, 403)
        self.assertEqual(self.client.delete(url).status_code, 204)

    def test_only_staff_can_create_notifications(self):
        payload = {'user': self.other.pk, 'title': 'Spam', 'description': 'd'}
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/notifications/list/', payload).status_code, 403)
        self.assertEqual(self.client.post('/api/notifications/categories/', {'name': 'x'}).status_code, 403)

        self.client.force_authenticate(self.staff)
        self.assertEqual(self.client.post('/api/notifications/list/', payload).status_code, 201)


class StaffOnlyContentTests(SecurityTestCase):
    def test_categories_writable_only_by_staff(self):
        category = Category.objects.create(name='Traktor')

        self.assertEqual(self.client.get('/api/market/categories/').status_code, 200)

        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/market/categories/', {'name': 'x'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/market/categories/{category.pk}/').status_code, 403)
        self.assertTrue(Category.objects.filter(pk=category.pk).exists())

        self.client.force_authenticate(self.staff)
        self.assertEqual(self.client.post('/api/market/categories/', {'name': 'Kombayn'}).status_code, 201)

    def test_banners_writable_only_by_staff(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get('/api/banners/').status_code, 200)
        self.assertEqual(self.client.post('/api/banners/', {'name': 'x', 'description': 'y'}).status_code, 403)


class RenterOnlyListingTests(SecurityTestCase):
    rent_payload = {
        'name': 'MTZ', 'equipment_name': 'Traktor', 'brand': 'MTZ', 'hp': 80, 'condition': 'yaxshi',
        'price': '100000', 'region': 'Toshkent', 'location_name': 'Chirchiq',
    }

    def market_payload(self, category):
        return {
            'category': category.pk, 'name': 'Urug\'', 'price': '5000', 'location': 'Toshkent',
            'condition': 'yangi', 'brand': 'b', 'model': 'm', 'description': 'd', 'phone_number': '+998900000000',
        }

    def test_non_renter_cannot_create_rent_item(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/rent/items/', self.rent_payload).status_code, 403)

        self.client.force_authenticate(self.renter)
        self.assertEqual(self.client.post('/api/rent/items/', self.rent_payload).status_code, 201)

    def test_non_renter_cannot_create_market_item(self):
        category = Category.objects.create(name='Urug\'lar')
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.post('/api/market/items/', self.market_payload(category)).status_code, 403)

        self.client.force_authenticate(self.renter)
        self.assertEqual(self.client.post('/api/market/items/', self.market_payload(category)).status_code, 201)

    def test_market_item_owner_and_staff_can_edit(self):
        category = Category.objects.create(name='Urug\'lar')
        item = MarketItem.objects.create(seller=self.renter, **{**self.market_payload(category), 'category': category})
        url = f'/api/market/items/{item.pk}/'

        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.patch(url, {'name': 'x'}).status_code, 403)

        self.client.force_authenticate(self.renter)
        self.assertEqual(self.client.patch(url, {'name': 'Egasi'}).status_code, 200)

        self.client.force_authenticate(self.staff)
        self.assertEqual(self.client.patch(url, {'name': 'Admin'}).status_code, 200)


@override_settings(STORAGES={
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
})
class AdminAccessKeyTests(SecurityTestCase):
    def setUp(self):
        super().setUp()
        self.superuser = make_user('+998900000005', is_staff=True, is_superuser=True)
        self.client.force_login(self.superuser)

    @override_settings(ADMIN_ACCESS_KEY='')
    def test_admin_closed_when_key_not_configured(self):
        self.assertEqual(self.client.get('/admin/?access=').status_code, 404)
        self.assertEqual(self.client.get('/admin/?access=agroterra_premium_2026').status_code, 404)

    @override_settings(ADMIN_ACCESS_KEY='yangi-maxfiy-kalit')
    def test_admin_requires_correct_key(self):
        self.assertEqual(self.client.get('/admin/?access=agroterra_premium_2026').status_code, 404)
        self.assertEqual(self.client.get('/admin/?access=yangi-maxfiy-kalit').status_code, 200)


class LoginTests(SecurityTestCase):
    def login(self, phone, password='Str0ng-pass!'):
        return self.client.post('/api/users/login/', {'phone_number': phone, 'password': password})

    def test_login_with_or_without_plus(self):
        # Foydalanuvchi "+998900000001" bilan saqlangan
        self.assertEqual(self.login('+998900000001').status_code, 200)
        self.assertEqual(self.login('998900000001').status_code, 200)
        self.assertEqual(self.login('+998 90 000-00-01').status_code, 200)
        self.assertEqual(self.login('998900000001', 'wrong').status_code, 400)

    def test_login_picks_account_matching_password(self):
        # Bir raqam ikki formatda, ikki xil hisob sifatida saqlangan holat
        plain = User.objects.create_user(phone_number='998900000004', password='Boshqa-pass1', first_name='A', last_name='B')
        response = self.login('998900000004')  # self.staff ("+998900000004") paroli
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], self.staff.id)
        response = self.login('+998900000004', 'Boshqa-pass1')
        self.assertEqual(response.data['user']['id'], plain.id)

    def test_popular_equipment_is_public(self):
        self.assertEqual(self.client.get('/api/popular-equipment/').status_code, 200)
