from django.shortcuts import render, HttpResponseRedirect
from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, User
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from mixins.views import TitleMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import auth
from django.views.generic import UpdateView


# Create your views here.

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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
