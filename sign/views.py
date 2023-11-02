from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import BaseRegisterForm, ConfirmRegisterForm
from .models import RegUser
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
import random
from datetime import datetime, timedelta


class BaseRegisterView(CreateView):
    model = RegUser
    form_class = BaseRegisterForm
    template_name = 'simple_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['text'] = 'Заполните форму.'
        return context

    def form_valid(self, form):
        reg_user = form.save(commit=True)
        reg_user.code = ''.join(random.choice('0123456789') for x in range(6))
        try:
            send_mail(
                subject='Регистрация нового пользователя',
                message='Ваш одноразовый код: ' + reg_user.code,
                from_email='pythontestuser@yandex.ru',
                recipient_list=[reg_user.email, ]
            )
        except:
            messages.error(self.request, 'При отправлении e-mail произошла ошибка.')
        return super().form_valid(form)


def confirm_email(request, pk):
    # сначала почистим временную БД
    old_reg_users = RegUser.objects.all().exclude(datetime__gt=datetime.now() - timedelta(minutes=2))
    old_reg_users.delete()
    # если записи нет
    if not RegUser.objects.filter(pk=pk).exists():
        return render(request, 'message.html', {
            'title': 'Регистрация', 'text': 'Временный код устарел. Вам необходимо пройти регистрацию заново.'})
    # если попытки закончились
    reg_user = RegUser.objects.get(pk=pk)
    if reg_user.approach >= 2:
        return render(request, 'message.html', {
            'title': 'Регистрация', 'text': 'Вы использовали все попытки.'})
    # подготовим данные вывода
    form = ConfirmRegisterForm()
    text = 'На вашу электронную почту было отправлено письмо с кодом подтверждения регистрации.'
    text_extra = 'Введите код из полученного письма.'
    # если введён код
    if request.method == 'POST':
        form = ConfirmRegisterForm(request.POST)
        if form.is_valid():
            # код введён верно
            if reg_user.code == request.POST.get('code'):
                user = User(
                    username=reg_user.username,
                    first_name=reg_user.first_name,
                    last_name=reg_user.last_name,
                    email=reg_user.email,
                    is_superuser=False,
                    is_staff=False
                )
                user.set_password(reg_user.password)
                user.save()
                reg_user.delete()
                return render(request, 'message.html', {
                    'title': 'Регистрация', 'text': 'Регистрация успешно завершена.'})
            # код введён неверно
            else:
                reg_user.approach += 1
                reg_user.save()
                text_extra = 'Неверный код. Попробуйте ещё раз. Осталось попвток: '+str(3-reg_user.approach)
    return render(request, 'simple_form.html', {
        'title': 'Регистрация', 'form': form, 'text': text, 'text_extra': text_extra})

