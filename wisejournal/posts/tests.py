from django.test import TestCase, Client

from .factories import UserFactory, GroupFactory, user_password
from .models import Post


class TestClientMixin:
    """Для установки Client в начале теста"""
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass


class TestIndexPage(TestClientMixin, TestCase):
    """Тесты для главной страницы"""
    def test_index_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestProfilePage(TestClientMixin, TestCase):
    """Тесты для страницы профиля пользователя"""
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()

    def test_get_profile_for_new_user_not_logged(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)


class TestGroupPage(TestClientMixin, TestCase):
    """Тесты для страницы сообщества"""
    def setUp(self):
        self.client = Client()
        self.group = GroupFactory()

    def test_get_real_group_page(self):
        response = self.client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)


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
            '/new/',
            data={
                'text': 'test text',
                'group': f'{group_id}'
            }
        )
        self.assertTrue(Post.objects.filter(text='test text', group=f'{group_id}'))


class TestNonAuthorizedUser(TestClientMixin, TestCase):
    """Тесты для проверки возможности не авторизированного пользователя"""
    def test_create_new_post_non_authorized_user(self):
        """
        Неавторизованный посетитель не может опубликовать пост
        (редирект на страницу входа)
        """
        group = GroupFactory()
        group_id = group.id

        response = self.client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': f'{group_id}'
            }
        )
        self.assertRedirects(
            response,
            expected_url='/auth/login/?next=/new/',
            status_code=302,
            target_status_code=200
        )


class TestNewPost(TestClientMixin, TestCase):
    """Тесты для проверки отображения поста на разных страницах"""
    def setUp(self):
        self.client = Client()

        self.user = UserFactory()
        login = self.client.login(username=self.user.username, password=user_password)
        self.assertTrue(login)

        self.group = GroupFactory()
        group_id = self.group.id

        self.client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': f'{group_id}'
            }
        )

    def test_new_post_on_index_page(self):
        response = self.client.get('/')
        self.assertContains(response=response, text='test text')

    def test_new_post_on_profile_page(self):
        response = self.client.get(f'/{self.user}/')
        self.assertContains(response=response, text='test text')

    def test_new_post_page_after_creation(self):
        response = self.client.get(f'/{self.user}/1/')
        self.assertContains(response=response, text='test text')


class TestEditPost(TestClientMixin, TestCase):
    """Тесты для проверки возможности редактирования поста"""
    def setUp(self):
        self.client = Client()

        self.user = UserFactory()
        login = self.client.login(username=self.user.username, password=user_password)
        self.assertTrue(login)

        self.group = GroupFactory()

        # Создания поста
        self.client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': f'{self.group.id}'
            }
        )

        # Редактирования нового поста
        self.client.post(
            f'/{self.user}/1/edit/',
            data={
                'text': 'new text!',
                'group': f'{self.group.id}'
            }
        )
        self.assertTrue(Post.objects.filter(text='new text!', group=self.group.id).exists())

    def test_edit_post(self):
        """Пользователь может редактировать пост повторно"""
        self.client.post(
            f'/{self.user}/1/edit/',
            data={
                'text': 'test edit post 124!',
                'group': f'{self.group.id}'
            }
        )
        self.assertTrue(Post.objects.filter(text='test edit post 124!', group=self.group.id).exists())

    def test_check_edit_post_on_index_page(self):
        response = self.client.get('/')
        self.assertContains(response=response, text='new text!')

    def test_check_edit_post_on_post_page(self):
        response = self.client.get(f'/{self.user}/1/')
        self.assertContains(response=response, text='new text!')

    def test_check_edit_post_on_profile_page(self):
        response = self.client.get(f'/{self.user}/')
        self.assertContains(response=response, text='new text!')
