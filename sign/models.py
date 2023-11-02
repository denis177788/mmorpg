from django.db import models
from django.urls import reverse


class RegUser(models.Model):

    # Модель для хранения одноразовых кодов,
    # а также другой информации при регистрации пользователей.

    # Примечание.
    # Данные из этой модели удаляются автоматически.
    # Это реализовано в функции confirm_email (модуль sign/views.py)
    # Функция устроена таким образом, что временный код не будет работать спустя 2 минуты,
    # даже если физическое удаление заиси из БД произойдёт позднее.

    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=128)
    code = models.CharField(max_length=10)
    approach = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pk} {self.datetime} {self.username}'

    # добавим url, чтобы после создания нас перебрасывало на страницу с pk
    def get_absolute_url(self):
        return reverse('confirm_email', args=[str(self.id)])



