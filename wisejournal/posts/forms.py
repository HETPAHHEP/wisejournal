from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Форма для нового поста пользователя
    """
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'text': 'Текст',
            'group': 'Сообщество',
            'image': 'Изображение'
        }
        help_texts = {
            'text': 'Брат, это поле для щитпоста',
            'group': 'Помоги другим бро по секте найти твой щитпост',
            'image': 'Покажи всем свой кринж'
        }
