from django import forms
from .models import Post, Message
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    text = forms.CharField(
        label='Текст',
        # widget=forms.Textarea,
        widget=CKEditorWidget()
    )
    # Если будут проблемы с виджетом "ckeditor", в папке "static" нужна папка "ckeditor".
    # Я её временно переименовал в "__ckeditor", так как она очень большая и не грузится на "github".

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'text': 'Основной текст',
        }


class MessageForm(forms.Form):
    text = forms.CharField(label='Текст', widget=forms.Textarea,
                           error_messages={'required': 'Это поле является обязательным.'})

