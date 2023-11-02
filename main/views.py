from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Message
from .filters import PostFilter, InboxFilter, OutboxFilter
from django.urls import reverse_lazy
from .forms import PostForm, MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class PostList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class MyPostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'my_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(user = self.request.user).order_by('-datetime')
        return queryset


class InboxList(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'inbox.html'
    context_object_name = 'messages_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Message.objects.filter(recipient=self.request.user).order_by('-datetime')
        self.filterset = InboxFilter(self.request.GET, queryset, request=self.request.user.pk)
        return self.filterset.qs    # queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class OutboxList(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'outbox.html'
    context_object_name = 'messages_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Message.objects.filter(sender=self.request.user).order_by('-datetime')
        self.filterset = OutboxFilter(self.request.GET, queryset)
        return self.filterset.qs    # queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):

    # если пользователь не залогинен -> на страницу залогинивания!
    login_url = '/sign/login/'
    redirect_field_name = 'redirect_to'

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('my_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новое объявление'
        return context


class PostEdit(LoginRequiredMixin, UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('my_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование объявления'
        return context


class PostDelete(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('my_posts')


class MessageDetail(DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

    # Если получатель впервые читает сообщение, то пометим его как прочитанное
    def get(self, request, **kwargs):
        msg = Message.objects.get(pk=self.kwargs['pk'])
        if (msg.recipient == self.request.user) and not msg.isread:
            msg.isread = True
            msg.save()
        return super().get(request, **kwargs)


def send_message(request, pk):
    primary = (request.path[1:5] == 'post')
    # если сообщение первичное
    if primary:
        form = MessageForm()
    # если сообщение является ответом на другое сообщение
    else:
        form = MessageForm(initial={'text': 'Здравствуйте! Я принимаю Ваш отклик!'})
    # если POST
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # сохраняем наше сообщение
            new_msg = Message(
                sender=request.user,
                text=form.cleaned_data['text'],
            )
            if primary:
                original_post = Post.objects.get(pk=pk)
                new_msg.post = original_post
                new_msg.recipient = original_post.user
            else:
                original_msg = Message.objects.get(pk=pk)
                new_msg.post = original_msg.post
                new_msg.recipient = original_msg.sender
            new_msg.save()
            # send e-mail
            if new_msg.recipient != '':
                try:
                    send_mail(
                        subject='Новое сообщение от пользователя ' + request.user.username,
                        message=new_msg.text,
                        from_email='pythontestuser@yandex.ru',
                        recipient_list=[new_msg.recipient.email, ]
                    )
                except:
                    messages.error(request, 'При отправлении e-mail произошла ошибка.')
            # redirect
            return redirect('/outbox/')
    return render(request, 'simple_form.html', {'title': 'Отправить отклик', 'form': form})


class MessageDelete(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'delete.html'
    success_url = reverse_lazy('inbox')


def emailing(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            for user in User.objects.all():
                if user.email:
                    try:
                        send_mail(
                            subject='Почтовая рассылка',
                            message=form.cleaned_data['text'],
                            from_email='pythontestuser@yandex.ru',
                            recipient_list=[user.email, ]
                        )
                        messages.info(request, 'Сообщение успешно отправлено. Адресат: ' + user.email)
                    except:
                        messages.error(request, 'При отправлении e-mail произошла ошибка. Адресат: ' + user.email)
            # redirect
            return render(request, 'message.html', {
                'title': 'Почтовая рассылка', 'text': 'Почтовая рассылка завершена.'})
    return render(request, 'simple_form.html', {
        'title': 'Почтовая рассылка', 'text': 'Введите текст почтовой рассылки.', 'form': form})


