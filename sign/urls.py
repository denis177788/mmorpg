from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .views import BaseRegisterView, confirm_email

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('signup/<int:pk>', confirm_email, name='confirm_email'),
    path('signup_info/', TemplateView.as_view(template_name="signup_info.html"), name='signup_info'),
]