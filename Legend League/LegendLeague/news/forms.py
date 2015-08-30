#encoding: utf-8

from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from news.models import *

class NoticiaForm(ModelForm):
    class Meta:
        model=New