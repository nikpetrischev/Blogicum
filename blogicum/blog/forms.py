# Standart Library
from datetime import datetime
from typing import Any

# Django Library
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Local Imports
from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('is_published', 'author')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'value': datetime.now().strftime('%Y-%m-%dT%H:%M'),
                },
            ),
        }


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='Текст комментария',
        required=True,
        widget=forms.Textarea(attrs={'rows': '4'}),
    )

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        max_length=254,
        required=False,
        widget=forms.TextInput(),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=False,
        widget=forms.TextInput(),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit: bool = True) -> Any:
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
