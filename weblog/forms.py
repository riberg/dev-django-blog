from urllib import request
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputUsername',
            'placeholder': 'Имя пользователя',
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputPassword',
            'placeholder': 'Пароль',
        }),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-2',
            'id': 'reInputPassword',
            'placeholder': 'Повторите пароль',
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

    def clean_username(self):
        username = self.cleaned_data['username']
        duplicate_user = User.objects.filter(username__iexact=username)
        if duplicate_user.exists():
            raise forms.ValidationError(
                "Пользователь с таким именем уже существует")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputUsername',
            'placeholder': 'Имя пользователя',
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mt-2',
            'id': 'inputPassword',
            'placeholder': 'Пароль',
        })
    )


class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Ваше имя',
        })
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Ваша почта',
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': 'Тема',
        })
    )
    message = forms.CharField(
        max_length=100,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'message',
            'rows': 2,
            'placeholder': 'Ваше сообщение',
        })
    )
