from django.contrib import admin
from .models import Category, Post, Message
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(
        label='Описание',
        widget=forms.Textarea
        # widget=CKEditorUploadingWidget()
        # чтобы работал виджет "ckeditor", в папке "static" нужна папка "admin"
        # (я её переименовал в "__admin", так как она очень большая и не грузится на "github")
    )
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
    list_filter = ["category"]
    search_fields = ("title", "category__name")
    form = PostAdminForm

admin.site.register(Category)
# admin.site.register(Post)
admin.site.register(Message)
