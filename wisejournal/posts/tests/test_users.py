from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post
from .factories import (GroupFactory, PostWithoutImageFactory, UserFactory,
                        user_password)


class TestClientMixin:
    """Для установки Client в начале теста"""

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        cache.clear()


class TestAuthorizedUser(TestClientMixin, TestCase):
    """Тесты для проверки возможности авторизированного пользователя"""

    def setUp(self):
        self.client = Client()

        self.user = UserFactory()
        login = self.client.login(username=self.user.username, password=user_password)
        self.assertTrue(login)

    def test_authorized_user_create_post(self):
        """Авторизованный пользователь может опубликовать пост"""
        group = GroupFactory()
        group_id = group.id

        self.client.post(
            reverse('new_post'),
            data={
                'text': 'test text',
                'group': group_id
            }
        )
        self.assertTrue(Post.objects.filter(text='test text', group=f'{group_id}'))

    def test_comment_functions_for_authorized_user(self):
        post = PostWithoutImageFactory()

        self.client.post(
            reverse('add_comment', kwargs={'username': post.author, 'post_id': 1}),
            data={'text': 'test comment!'}
        )
        self.assertTrue(post.comments.filter(text='test comment!').exists())

    def test_follow_functions(self):
        following_author = UserFactory()

        # Проверка возможности подписаться
        self.client.get(reverse('profile_follow', kwargs={'username': following_author}))
        check_following = self.user.follower.filter(author=following_author).exists()
        self.assertTrue(check_following)

        # Проверка возможности отписаться
        self.client.get(reverse('profile_unfollow', kwargs={'username': following_author}))
        check_following = self.user.follower.filter(author=following_author).exists()
        self.assertFalse(check_following)


class TestNonAuthorizedUser(TestClientMixin, TestCase):
    """Тесты для проверки возможности не авторизированного пользователя"""

    def test_comment_functions_for_non_authorized_user(self):
        post = PostWithoutImageFactory()

        self.client.post(
            reverse('add_comment', kwargs={'username': post.author, 'post_id': 1}),
            data={'text': 'test comment!'}
        )
        self.assertFalse(post.comments.filter(text='test comment!').exists())

    def test_create_new_post_non_authorized_user(self):
        """
        Неавторизованный посетитель не может опубликовать пост
        (редирект на страницу входа)
        """
        group = GroupFactory()
        group_id = group.id

        response = self.client.post(
            reverse('new_post'),
            data={
                'text': 'test text',
                'group': group_id
            }
        )
        self.assertRedirects(
            response,
            expected_url='/auth/login/?next=/new/',
            status_code=302,
            target_status_code=200
        )
