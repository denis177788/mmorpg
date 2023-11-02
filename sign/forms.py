from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import RegUser
from django.core.exceptions import ValidationError


class BaseRegisterForm(forms.ModelForm):
    username = forms.CharField(min_length=5, max_length=30, label='Логин', error_messages={
        'required': 'Это поле является обязательным.',
        'min_length': 'Длина логина должна быть не меньше 5 символов.'})
    first_name = forms.CharField(max_length=30, label='Имя', error_messages={
        'required': 'Это поле является обязательным.'})
    last_name = forms.CharField(max_length=30, label='Фамилия', error_messages={
        'required': 'Это поле является обязательным.'})
    email = forms.EmailField(max_length=30, label='e-mail', error_messages={
        'required': 'Это поле является обязательным.',
        'invalid': 'Введите корректный e-mail адрес.'})
    password = forms.CharField(min_length=5, max_length=30, widget=forms.PasswordInput(), label='Пароль', error_messages={
        'required': 'Это поле является обязательным.',
        'min_length': 'Длина пароля должна быть не меньше 5 символов.'})
    password_verify = forms.CharField(min_length=5, max_length=30, widget=forms.PasswordInput(), label='Повторите пароль', error_messages={
        'required': 'Это поле является обязательным.',
        'min_length': 'Длина пароля должна быть не меньше 5 символов.'})

    class Meta:
        model = RegUser
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password",
                  )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_verify = cleaned_data.get("password_verify")
        if password != password_verify:
            raise ValidationError('Пароли не совпадают.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой логин уже используется.')
        return username


class ConfirmRegisterForm(forms.Form):
    code = forms.CharField(min_length=6, max_length=6, label='Код', error_messages={
        'required': 'Это поле является обязательным.',
        'min_length': 'Длина кода должна равняться 6 символов.'})








