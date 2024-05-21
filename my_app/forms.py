from django import forms
from django.contrib.auth.models import User

from .models import Article, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = "__all__"
        fields = ['title', 'content', 'image', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Maqola Nomi',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Maqola Matni',
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'from-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Foydalanuvchi ismi",
                               widget=forms.TextInput(attrs={
                                   "class": 'form-control',
                               }))
    password = forms.CharField(label="Foydalanuvchi paroli",
                               widget=forms.PasswordInput(attrs={
                                   "class": "form-control"
                               }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, help_text="Maksium 150 ta simvol",
                               widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "Foydalanuvchi ismi",
                                   "style": 'margin:20px 20px 20px 0px; width:300px'
                               }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Parol",
        "style": 'margin:20px 20px 20px 0px; width:300px'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Parolni tasdiqlash",
        "style": 'margin:20px 20px 20px 0px; width:300px'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        'placeholder': "Email",
        "style": 'margin:20px 20px 20px 0px; width:300px'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Sizning commentingiz"
            })
        }
