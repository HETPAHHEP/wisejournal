import os
import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from .factories import UserFactory, GroupFactory, PostWithoutImageFactory, user_password
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
        response = self.client.get(
            reverse('index')
        )
        self.assertEqual(response.status_code, 200)


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
            reverse('new_post'),
            data={
                'text': 'test text',
                'group': group_id
            }
        )

    def test_new_post_on_index_page(self):
        response = self.client.get(
            reverse('index')
        )
        self.assertContains(response=response, text='test text')

    def test_new_post_on_profile_page(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user})
        )
        self.assertContains(response=response, text='test text')

    def test_new_post_page_after_creation(self):
        response = self.client.get(
            reverse('post', kwargs={'username': self.user, 'post_id': 1})
        )
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
            reverse('new_post'),
            data={
                'text': 'test text',
                'group': self.group.id
            }
        )

        # Редактирования нового поста
        self.client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user,
                    'post_id': 1
                }
            ),
            data={
                'text': 'new text!',
                'group': self.group.id
            }
        )
        self.assertTrue(Post.objects.filter(text='new text!', group=self.group.id).exists())

    def test_edit_post(self):
        """Пользователь может редактировать пост повторно"""
        self.client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user,
                    'post_id': 1
                }
            ),
            data={
                'text': 'test edit post 124!',
                'group': self.group.id
            }
        )
        self.assertTrue(Post.objects.filter(text='test edit post 124!', group=self.group.id).exists())

    def test_check_edit_post_on_index_page(self):
        response = self.client.get(
            reverse('index')
        )
        self.assertContains(response=response, text='new text!')

    def test_check_edit_post_on_post_page(self):
        response = self.client.get(
            reverse('post', kwargs={'username': self.user, 'post_id': 1})
        )
        self.assertContains(response=response, text='new text!')

    def test_check_edit_post_on_profile_page(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user})
        )
        self.assertContains(response=response, text='new text!')


class TestPageNotFound404(TestClientMixin, TestCase):
    """Тесты для проверки страницы с ошибкой 404"""

    def test_try_to_get_fake_page(self):
        response = self.client.get('/this-page-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, template_name='misc/404.html')


class TestImages(TestClientMixin, TestCase):
    """Тесты для проверки изображений постов"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media_root = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(cls.temp_media_root)  # noqa

    def setUp(self):
        # Файлы для теста. Необходимы для функционирования!
        self.image_for_test = 'media/tests_source/for_test.jpg'
        self.non_image_file_for_test = 'media/tests_source/poem'

        # Изменяем MEDIA_ROOT на временную папку
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.temp_media_root

        # Создание данных для поста и логин
        self.client = Client()
        self.user = UserFactory()
        login = self.client.login(username=self.user.username, password=user_password)
        self.assertTrue(login)
        self.post = PostWithoutImageFactory(text='text without pic/image', author=self.user)
        self.assertTrue(self.post)

    def tearDown(self):
        # Возвращаем MEDIA_ROOT в исходное состояние
        settings.MEDIA_ROOT = self.original_media_root

        # Для проверки путей временных файлов при тесте
        # print(self, self.temp_media_root)

        # Удаляем все файлы из временной папки
        shutil.rmtree(self.temp_media_root)
        os.mkdir(self.temp_media_root)

        super().tearDown()

    def test_image_exists(self):
        # Добавление картинки к существующему посту
        with open(self.image_for_test, 'rb') as img:
            post_with_image = self.client.post(
                reverse(
                    'post_edit',
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }
                ),
                data={
                    'text': 'post with image',
                    'group': self.post.group.id,
                    'image': img
                }
            )

        post_url = reverse('post', kwargs={'username': self.user, 'post_id': self.post.id})

        self.assertRedirects(
            post_with_image,
            expected_url=post_url,
            status_code=302,
            target_status_code=200
        )

        response = self.client.get(post_url)
        self.assertContains(response=response, text='<img class')

    def test_display_post_image_on_all_linked_pages(self):
        # Добавление картинки к существующему посту
        with open(self.image_for_test, 'rb') as img:
            post_with_image = self.client.post(
                reverse(
                    'post_edit',
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }
                ),
                data={
                    'text': 'post with image',
                    'group': self.post.group.id,
                    'image': img
                }
            )

        post_url = reverse('post', kwargs={'username': self.user, 'post_id': self.post.id})

        self.assertRedirects(
            post_with_image,
            expected_url=post_url,
            status_code=302,
            target_status_code=200
        )

        # Проверка страниц, где должен быть пост
        urls = (
            reverse('index'),
            reverse('profile', kwargs={'username': self.user}),
            reverse('group', kwargs={'slug': self.post.group.slug})
        )

        for url in urls:
            response_index_page = self.client.get(url)
            self.assertContains(response=response_index_page, text='<img class')

    def test_upload_file_not_image_type(self):
        # Добавление отличного от картинки файла к существующему посту
        with open(self.non_image_file_for_test, 'rb') as file:
            post_with_file = self.client.post(
                reverse(
                    'post_edit',
                    kwargs={
                        'username': self.user,
                        'post_id': self.post.id
                    }
                ),
                data={
                    'text': 'post with image',
                    'group': self.post.group.id,
                    'image': file
                }
            )
            self.assertEqual(post_with_file.status_code, 200)
            # Проверяем, что на странице поста не отображается тег img
            self.assertNotContains(post_with_file, '<img class')
