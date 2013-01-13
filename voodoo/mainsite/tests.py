"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client
from django.contrib.auth.models import User


class TestViewsStatusCode(TestCase):

    def test_status_codes_200(self):
        self.client = Client()
        self.user = User.objects.create_user('root', 'lennon@thebeatles.com', '111')
        self.assertTrue(self.client.login(username='root', password='111'))
        self.assertEqual(self.client.get('/basket/').status_code, 200)
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/notice_of_payment/').status_code, 200)
        self.assertEqual(self.client.get('/order_dispatch/').status_code, 200)
        self.assertEqual(self.client.get('/orders/').status_code, 200)
        self.assertEqual(self.client.get('/prepays/').status_code, 200)
        self.assertEqual(self.client.get('/search_product/?detail_id=').status_code, 200)
        self.assertEqual(self.client.get('/sendings/').status_code, 200)
        self.assertEqual(self.client.get('/show_vin/').status_code, 200)
        self.assertEqual(self.client.get('/vin_request/').status_code, 200)

