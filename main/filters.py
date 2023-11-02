from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Category, Message
from django import forms
from django.contrib.auth.models import User


class PostFilter(FilterSet):

   category = ModelChoiceFilter(
       field_name='category__name',
       queryset=Category.objects.all(),
       label='По категории:',  # новое имя для поля
       empty_label='<любая>',  # заменяем чёрточки на "любой"
   )

   user = ModelChoiceFilter(
       field_name='user__username',
       queryset=User.objects.all(),
       label='По пользователю:',  # новое имя для поля
       empty_label='<любой>',  # заменяем чёрточки на "любой"
   )

   date = DateFilter(
       field_name='datetime',
       widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
       lookup_expr='gt',
       label='По дате (не старше):'
   )

   class Meta:
       model = Post
       fields = {
           # поиск по названию
           #'title': ['icontains'],
           # по категории
           #'category': ['exact'],
       }


class InboxFilter(FilterSet):

   post = ModelChoiceFilter(
       field_name='post',
       queryset=Post.objects.all(),
       label='По моим объявлениям:',
       empty_label='<все мои объявления>',
   )

   date = DateFilter(
       field_name='datetime',
       widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
       lookup_expr='gt',
       label='По дате (не старше):'
   )

   class Meta:
       model = Message
       fields = ('post', )

   def __init__(self, *args, **kwargs):
       super(InboxFilter, self).__init__(*args, **kwargs)
       self.filters['post'].queryset = Post.objects.filter(user_id=kwargs['request'])

class OutboxFilter(FilterSet):

   date = DateFilter(
       field_name='datetime',
       widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
       lookup_expr='gt',
       label='По дате (не старше):'
   )

   class Meta:
       model = Message
       fields = {
           #'text': ['icontains'],
       }