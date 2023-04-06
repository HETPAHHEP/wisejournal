from unittest import TestCase

from django.test import Client


class TestIndexPage(TestCase):
    def test_index_available(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
