import factory

from .models import User, Group, Post

from django.contrib.auth.hashers import make_password

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


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    text = factory.Sequence(lambda n: f'Test text numb-{n}')
    group = factory.SubFactory(GroupFactory)
    author = factory.SubFactory(UserFactory)
