from django import forms

from .models import Post, Comment


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


class CommentForm(forms.ModelForm):
    """
    Форма для комментария к конкретному посту
    """
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['text']
        help_texts = {'text': 'Написать мудрость'}
