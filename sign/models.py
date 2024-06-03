from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    def save(self, *args, **kwargs):
        user = super(BaseRegisterForm, self).save(*args, **kwargs)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

class BasicSignupForm(SignupForm):
    
    def save(self, *args, **kwargs):
        user = super(BasicSignupForm, self).save(*args, **kwargs)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )
