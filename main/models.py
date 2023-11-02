from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):

    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    # image1 = models.ImageField(upload_to='images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #def preview(self):
    #    return self.text[0:123]+'...'


class Message(models.Model):

    datetime = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    isread = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.datetime}] sener: [{self.sender}] recipient: [{self.recipient}] \
            text: [{self.text}] isread: [{self.isread}]'


# Примечание.
# Я использовал стандартную модель User для хранения данных о пользователях.
