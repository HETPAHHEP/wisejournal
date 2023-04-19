import factory
from django.contrib.auth.hashers import make_password

from ..models import Group, Post, User

user_password = 'password12345test'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'dima{n}')
    first_name = factory.Sequence(lambda n: f'dima{n}')
    email = factory.Sequence(lambda n: f'dima{n}@fbi.gov')
    password = make_password(user_password)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    title = 'Test title'
    slug = factory.Sequence(lambda x: f'group_{x}')
    description = 'empty'


class PostWithoutImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    text = factory.Sequence(lambda n: f'Test text numb-{n}')
    # Создается новая группа, если не передать в параметры
    group = factory.SubFactory(GroupFactory)
    # Создается новый пользователь, если не передать в параметры
    author = factory.SubFactory(UserFactory)
