from django import forms

from .models import Comment, Post


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
            'text': 'Поле для Вашей мудрости',
            'group': 'Распространите истину среди мудрецов конкретного общества',
            'image': 'Покажите мудрость, которую не видел ещё свет наш.'
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
