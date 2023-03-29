from django import forms
from django.contrib.auth import get_user_model

from .models import Post, Group


class PostForm(forms.ModelForm):
    """
    Форма для нового поста пользователя
    """
    class Meta:
        model = Post
        fields = ('group', 'text')
