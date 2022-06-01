from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Tweet

class ClientCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email',  'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(ClientCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})

            # field.widget.attrs.update({'class': name of css class <using bootstrap5>})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'lastname', 'email', 'profile_img','bio']
        labels = {
            'name': 'Name',
            'lastname': 'Last Name',
            'email': 'Email',
            'bio': 'Bio',
            
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control my-3',
            'placeholder': 'What\'s on your mind ?...',
            'rows': '5'})

        # Attrs keywords are from bootstrap