from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import LoginForm, UserCreateForm


# Create your views here.

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
               login(request, user)
               next_url = request.GET.get('next', 'index')
               return redirect(next_url)
            form = LoginForm()
        return render(request, 'login.html', {'form': form})

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class UserCreateView(CreateView):

    model = User
    form_class = UserCreateForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')