from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from .factories import (GroupFactory, PostWithoutImageFactory, UserFactory,
                        user_password)


class TestClientMixin:
    """Для установки Client в начале теста"""

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        cache.clear()


class TestIndexPage(TestClientMixin, TestCase):
    """Тесты для главной страницы"""

    def test_index_available(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_check_caching(self):
        PostWithoutImageFactory()

        with self.assertNumQueries(5):
            response = self.client.get(reverse('index'))
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('index'))
            self.assertEqual(response.status_code, 200)


class TestFollowingPage(TestClientMixin, TestCase):
    """Тесты для проверки страницы подписки"""

    def setUp(self):
        self.client = Client()

        self.user = UserFactory()
        login = self.client.login(username=self.user.username, password=user_password)
        self.assertTrue(login)

        self.author = UserFactory()
        self.post = PostWithoutImageFactory(author=self.author)

    def test_check_post_on_following_page_for_follower(self):
        self.client.get(reverse('profile_follow', kwargs={'username': self.author}))
        check_following = self.user.follower.filter(author=self.author).exists()
        self.assertTrue(check_following)

        with self.assertNumQueries(7):
            self.client.get(reverse('follow_index'))

    def test_check_post_on_following_page_for_non_follower(self):
        with self.assertNumQueries(3):
            self.client.get(reverse('follow_index'))


class TestProfilePage(TestClientMixin, TestCase):
    """Тесты для страницы профиля пользователя"""

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_get_profile_for_new_user_not_logged(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)


class TestGroupPage(TestClientMixin, TestCase):
    """Тесты для страницы сообщества"""

    def setUp(self):
        self.client = Client()
        self.group = GroupFactory()

    def test_get_real_group_page(self):
        response = self.client.get(
            reverse('group', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.status_code, 200)


class TestPageNotFound404(TestClientMixin, TestCase):
    """Тесты для проверки страницы с ошибкой 404"""

    def test_try_to_get_fake_page(self):
        response = self.client.get('/this-page-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, template_name='misc/404.html')
