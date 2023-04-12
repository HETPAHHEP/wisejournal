from django.test import TestCase, Client

from .models import User, Post, Group

class TestClientMixin:
    def setUp(self):
        self.client = Client()

    def tearDown(self):
       pass


class TestIndexPage(TestClientMixin, TestCase):
    def test_index_available(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestProfilePage(TestClientMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        )

    def tearDown(self):
        User.objects.filter(
            username='new_user_test',
            email='test@mail.com'
        ).delete()

    def test_get_profile_for_new_user_not_logged(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)


class TestAuthorizedUser(TestClientMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        )
        self.client.login(username=self.user.username, password='12345')

    def tearDown(self):
        Group.objects.filter(
            title='test',
            slug='test',
            description='test'
        ).delete()

        User.objects.filter(
            username='new_user_test',
            email='test@mail.com'
        ).delete()

    def test_authorized_user_create_post(self):
        group = Group.objects.create(
            title='test',
            slug='test',
            description='test'
        )
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
    def tearDown(self):
        Group.objects.filter(
            title='test',
            slug='test',
            description='test'
        ).delete()

    def test_create_new_post_non_authorized_user(self):
        group = Group.objects.create(
            title='test',
            slug='test',
            description='test'
        )
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
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        )
        self.client.login(username=self.user.username, password='12345')

        self.group = Group.objects.create(
            title='test',
            slug='test',
            description='test'
        )
        group_id = self.group.id

        self.client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': f'{group_id}'
            }
        )

    def tearDown(self):
        User.objects.filter(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        ).delete()

        Group.objects.filter(
            title='test',
            slug='test',
            description='test'
        ).delete()

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
    def setUp(self):
        self.client = Client()

        self.user = self.user = User.objects.create_user(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        )
        self.client.login(username=self.user.username, password='12345')

        self.group = Group.objects.create(
            title='test',
            slug='test',
            description='test'
        )

        self.client.post(
            '/new/',
            data={
                'text': 'test text',
                'group': f'{self.group.id}'
            }
        )

        self.client.post(
            f'/{self.user}/1/edit/',
            data={
                'text': 'new text!',
                'group': f'{self.group.id}'
            }
        )

    def tearDown(self):
        User.objects.filter(
            username='new_user_test',
            email='test@mail.com',
            password='12345'
        ).delete()

        Group.objects.filter(
            title='test',
            slug='test',
            description='test'
        ).delete()

    def test_edit_post(self):
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
