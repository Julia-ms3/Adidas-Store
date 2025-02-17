from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from mixins.views import TitleMixin
from users.forms import (User, UserLoginForm, UserProfileForm,
                         UserRegistrationForm)
from users.models import EmailVerification


class UserRegistrationView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'You have successfully registered'
    title = 'Registration'


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Login'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm
    title = 'Profile'


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Email Confirmation'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect(reverse('index'))
