from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    TestScoresUpdateForm
)
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        t_form = TestScoresUpdateForm(request.POST,
                                      instance=request.user.testscores)
        if u_form.is_valid() and p_form.is_valid() and t_form.is_valid():
            u_form.save()
            p_form.save()
            t_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        t_form = TestScoresUpdateForm(instance=request.user.testscores)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        't_form': t_form
    }
    return render(request, 'users/profile.html', context)
