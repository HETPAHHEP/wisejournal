from django.test import TestCase, Client


class TestFlatpages(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_about_author_page(self):
        response = self.client.get('/about/about-author/')
        self.assertEqual(response.status_code, 200)

    def test_get_about_spec(self):
        response = self.client.get('/about/about-spec/')
        self.assertEqual(response.status_code, 200)
