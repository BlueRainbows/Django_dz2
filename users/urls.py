from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users.views import ProfileView, VerificationView, activate, RegisterView, reset_password


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('register/', RegisterView.as_view(), name='register'),
    path('verification/', VerificationView.as_view(), name='verification'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('activate/success', TemplateView.as_view(template_name='users/activation_success.html'), name='success_activate'),
    path('activate/error', TemplateView.as_view(template_name='users/activation_error.html'), name='error_activate'),

    path('reset_password/', reset_password, name='reset_password'),
    path('password_reset_complete/', TemplateView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    ]