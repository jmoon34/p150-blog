from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, TestScores

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class TestScoresUpdateForm(forms.ModelForm):
    class Meta:
        model = TestScores
        fields = ['two_k', 'six_k', 'max_watts']
        labels = {
            'two_k': '2k',
            'six_k': '6k',
            'max_watts': 'Max Watts'
        }
