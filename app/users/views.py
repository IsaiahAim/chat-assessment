from django.contrib.auth.models import User
from .forms import UserUpdateForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction


@login_required(login_url="user_login")
def chat_view(request):
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, "chat.html", {'users': users, 'authenticated_user': request.user})


# User registration.
@transaction.atomic
def create_user(request):
    template_name = "users/register.html"
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data['password'])
            user.save()
            message = f"account with {form.cleaned_data['username']} has been created"
            messages.success(request, f'{message}')
            return redirect('chat_view')
        messages.success(request, 'could not complete registration.')
        return redirect('create_user')
    form = UserRegistrationForm()
    context = {"form": form}
    return render(request, template_name, context)


def user_login(request):
    template_name = "users/login.html"
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect("chat_view")
            messages.warning(request, f"Invalid username or password")
            return redirect('user_login')
        messages.warning(request, f"{form.error_messages}")
        return redirect('user_login')
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, template_name, context)


# User logout.


def user_logout(request):
    logout(request)
    messages.success(request, f"Logout successful.")
    return redirect("user_login")
