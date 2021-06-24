from django.contrib.auth import authenticate, login as login_user
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, UpdateView

from .models import Accounts
from .forms import AccountForm


class AccountCreation(CreateView):
    form_class = AccountForm
    template_name = 'accounts/signup.html'
    model = Accounts
    success_message = "Account created successfully"


class Payment(TemplateView):
    template_name = 'accounts/payment.html'


class UpdateProfile(UpdateView):
    model = Accounts
    fields = ['first_name', 'last_name', 'mobile', 'email', 'address']
    template_name_suffix = '_update_form'
    success_url = '/management/profile'




def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login_user(request, user)
                return redirect(reverse('management:profile'))
        else:
            messages.error(request, 'username or password not correct')
            return redirect(reverse('accounts:login'))

    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
