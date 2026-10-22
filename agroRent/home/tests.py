from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase

from agroRent.utils.translator import translate_many, BLOCK_KEY
from home.models import SiteText
from rent.models import RentItem
from users.models import User


@override_settings(AUTO_TRANSLATE=True)
class TranslatorTests(TestCase):
    def setUp(self):
        cache.clear()
        patcher = patch('agroRent.utils.translator.GoogleTranslator')
        self.google = patcher.start().return_value
        self.google.translate.side_effect = lambda text: text.upper()
        self.addCleanup(patcher.stop)

    def test_single_line_texts_are_sent_in_one_request_and_cached(self):
        texts = ['tractor for rent', 'good condition', 'tractor for rent']
        result = translate_many(texts, 'ru')
        self.assertEqual(result, {'tractor for rent': 'TRACTOR FOR RENT', 'good condition': 'GOOD CONDITION'})
        self.assertEqual(self.google.translate.call_count, 1)

        # Ikkinchi marta Google'ga so'rov ketmaydi
        translate_many(texts, 'ru')
        self.assertEqual(self.google.translate.call_count, 1)

    def test_falls_back_to_one_by_one_when_lines_merge(self):
        self.google.translate.side_effect = lambda text: text.replace('\n', ' ').upper()
        result = translate_many(['first line text', 'second line text'], 'ru')
        self.assertEqual(result['first line text'], 'FIRST LINE TEXT')
        self.assertEqual(result['second line text'], 'SECOND LINE TEXT')

    def test_google_failure_pauses_translation(self):
        self.google.translate.side_effect = Exception('Too many requests')
        self.assertEqual(translate_many(['some english text'], 'ru'), {'some english text': 'some english text'})
        self.assertTrue(cache.get(BLOCK_KEY))

        # Bloklangan paytda Google'ga umuman murojaat qilinmaydi
        self.google.translate.reset_mock()
        translate_many(['another english text'], 'ru')
        self.google.translate.assert_not_called()


@override_settings(AUTO_TRANSLATE=True)
class ListTranslationTests(APITestCase):
    def test_whole_list_is_translated_in_one_batch(self):
        owner = User.objects.create_user(phone_number='+998900000009', password='x', first_name='A', last_name='B', is_renter=True)
        for i in range(5):
            RentItem.objects.create(owner=owner, name=f'Item {i}', equipment_name='Traktor', brand='MTZ', hp=80,
                                    condition='yaxshi', price=1000, region='Toshkent', location_name='Chirchiq')

        with patch('agroRent.utils.mixins.translate_many', side_effect=lambda texts, lang: {t: t + '!' for t in texts}) as tm:
            response = self.client.get('/api/rent/items/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tm.call_count, 1)
        first = response.data['results'][0]
        self.assertTrue(first['name'].endswith('!'))
        self.assertTrue(first['owner_details']['street'] == '' or first['owner_details']['street'].endswith('!'))


@override_settings(AUTO_TRANSLATE=False)
class AutoTranslateDisabledTests(APITestCase):
    def setUp(self):
        cache.clear()
        patcher = patch('agroRent.utils.translator.GoogleTranslator')
        self.google_cls = patcher.start()
        self.addCleanup(patcher.stop)

    def test_list_is_returned_as_is_without_google(self):
        owner = User.objects.create_user(phone_number='+998900000009', password='x', first_name='A', last_name='B', is_renter=True)
        RentItem.objects.create(owner=owner, name='Traktor MTZ', equipment_name='Traktor', brand='MTZ', hp=80,
                                condition='yaxshi', price=1000, region='Toshkent', location_name='Chirchiq')
        response = self.client.get('/api/rent/items/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['name'], 'Traktor MTZ')
        self.google_cls.assert_not_called()

    def test_translate_view_uses_site_texts_only(self):
        SiteText.objects.create(key='Rent machinery', uz='Texnika ijarasi', ru='Аренда техники')
        response = self.client.post('/api/translate/', {'texts': ['Rent machinery', 'New text'], 'lang': 'ru'}, format='json')
        self.assertEqual(response.data, {'Rent machinery': 'Аренда техники', 'New text': 'New text'})
        # Yangi matn admin to'ldirishi uchun qo'shiladi, ruscha maydoni bo'sh qoladi
        new = SiteText.objects.get(key='New text')
        self.assertFalse(new.ru)
        self.google_cls.assert_not_called()
