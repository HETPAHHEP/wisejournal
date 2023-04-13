import factory
from .models import User, Group, Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'dima-{n}')
    first_name = factory.Sequence(lambda n: f'dima-{n}')
    email = factory.Sequence(lambda n: f'dima-{n}@fbi.gov')
    password = '12345'


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
