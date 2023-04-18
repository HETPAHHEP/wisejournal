from django.test import Client, TestCase
from django.urls import reverse


class TestFlatpages(TestCase):
    """Тесты проверки работоспособности простых страниц"""
    def setUp(self):
        self.client = Client()

    def test_get_about_author_page(self):
        response = self.client.get(
            reverse('about-author')
        )
        self.assertEqual(response.status_code, 200)

    def test_get_about_spec(self):
        response = self.client.get(
            reverse('about-spec')
        )
        self.assertEqual(response.status_code, 200)
