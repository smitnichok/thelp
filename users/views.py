from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import logout
from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm
from users.models import User


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        if self.request.user.role_id == 3:
            return '/empl/pageemp/'
        else:
            return '/helpdesk/mainpageusers/'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role_id = 2
        user.save()
        return super().form_valid(form)


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileEmpl(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/emplpfile.html'

    def get_success_url(self):
        return reverse_lazy('users:emplpfile')

    def get_object(self, queryset=None):
        return self.request.user


def logout_view(request):
    logout(request)
    return redirect('users:login')
