from django.forms import ModelForm
from api.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

from todo.models import Todo


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['name', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'id': 'name', 'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'id': 'description', 'class': 'form-control'}),
        }

class UserProfile(ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'phone', 'address','avatar']
        widgets = {
            'avatar' : forms.FileInput(attrs={'id': 'avatar', 'class': 'form-control'}),
            'fullname' : forms.TextInput(attrs={'id': 'fullname', 'class': 'form-control'}),
            'phone' : forms.TextInput(attrs={'id': 'phone', 'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'id': 'address', 'class': 'form-control'}),
        }

class UserChangePassword(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2' ]
        widgets = {
            'new_password1' : forms.TextInput(attrs={'id': 'new_password1', 'class': 'form-control'}),
            'new_password2' : forms.TextInput(attrs={'id': 'new_password2', 'class': 'form-control'}),
        }
