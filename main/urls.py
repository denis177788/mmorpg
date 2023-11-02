from django.urls import path
from .views import PostList, PostDetail, MyPostList, PostCreate, PostEdit, PostDelete, \
   InboxList, OutboxList, MessageDetail, MessageDelete, send_message, emailing


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('post/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('my_posts/', MyPostList.as_view(), name='my_posts'),
   path('inbox/', InboxList.as_view(), name='inbox'),
   path('outbox/', OutboxList.as_view(), name='outbox'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('post/<int:pk>/message/', send_message, name='send_message'),
   path('message/<int:pk>/', MessageDetail.as_view(), name='message_detail'),
   path('message/<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),
   path('message/<int:pk>/accept/', send_message, name='message_accept'),
   path('emailing/', emailing, name='emailing'),
]
